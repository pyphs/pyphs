# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 18:57:05 2016

@author: Falaize
"""

import numpy
from numpy import (cos, sin, pi,
                   arange,
                   linspace,
                   ones, zeros, ones_like,
                   vstack, hstack)
from numpy.random import uniform
from numpy import min as npmin
from numpy import max as npmax
from scipy.signal import chirp


_pars = {'SYNTH_OUT': 'array'}

names = ['zero', 'const', 'sin', 'cos', 'noise', 'step', 'sweep']

parameters = {'which': 'sin',
              'tsig': 1.,
              'ncycles': 1,
              'tdeb': 0,
              'tend': 0,
              'fs': int(48e3),
              'A': 1.,
              'A1': 0.,
              'f0': 10.,
              'f1': 100.,
              'cycle_ratio': 1.,
              'attack_ratio': 0.,
              'decay_ratio': 0.,
              'ramp_on': False,
              'bkgrd_noise': 0.}


def sine(n, fs, f0, A=1., f1=None, A1=1.):
    """
    Build a generator that yields a sine wave.

    Parameters
    ----------
    n : int
        Number of samples generated.
    fs : int
        Sample rate in Hz.
    f0 : float
        Sin frequency.
    A : float, optional
        Sine amplitude (the default is 1.0).
    f1 : float or None, optional
        Secondary sine frequency if float (the default is None).
    A1 : float, optional
        Secondary amplitude (the default is 1.0).

    Yields
    ------
    s : float
        Sequence of sine wave values.
    """

    if _pars['SYNTH_OUT'] == 'array':
        s = A*sin(2*pi*f0*numpy.arange(n)/fs)
        if isinstance(f1, (float, int)):
            s += A1*sin(2*pi*f1*numpy.arange(n)/fs)
        return s

    elif _pars['SYNTH_OUT'] == 'generator':
        for i in range(n):
            t = float(i)/fs
            val = A*sin(2*pi*f0*t)
            if isinstance(f1, (float, int)):
                val += A1*sin(2*pi*f1*t)
            yield val


def cosine(n, fs, f0, A=1., f1=None, A1=1.):
    """
    Build a generator that yields a cosine wave.

    Parameters
    ----------
    n : int
        Number of samples generated.
    fs : int
        Sample rate in Hz.
    f0 : float
        Sin frequency.
    A : float, optional
        Cosine amplitude (the default is 1.0).
    f1 : float or None, optional
        Secondary sine frequency if float (the default is None).
    A1 : float, optional
        Secondary amplitude (the default is 1.0).

    Yields
    ------
    s : float
        Sequence of cosine wave values.
    """
    if _pars['SYNTH_OUT'] == 'array':
        s = A*cos(2*pi*f0*numpy.arange(n)/fs)
        if isinstance(f1, (float, int)):
            s += A1*cos(2*pi*f1*numpy.arange(n)/fs)
        return s

    elif _pars['SYNTH_OUT'] == 'generator':
        for i in range(n):
            t = float(i)/fs
            val = A*cos(2*pi*f0*t)
            if isinstance(f1, (float, int)):
                val += A1*cos(2*pi*f1*t)
            yield val


def randomuniform(n, A=1.):
    """
    Build a generator that yields a noise distributed according uniform \
probability densisty.

    Parameters
    ----------
    n : int
        Number of samples generated.
    A : float, optional
        Noise amplitude (the default is 1.0).

    Yields
    ------
    s : float
        Sequence of noise values.
    """

    if _pars['SYNTH_OUT'] == 'array':
        return uniform(-A, A, n)

    elif _pars['SYNTH_OUT'] == 'generator':
        for i in range(n):
            yield uniform(-A, A)


def constant(n, A=1.):
    """
    Build a generator that yields a constant value.

    Parameters
    ----------
    n : int
        Number of samples generated.
    A : float, optional
        Constant (the default is 1.0).

    Yields
    ------
    s : float
        Sequence of constant value.
    """

    if _pars['SYNTH_OUT'] == 'array':
        return A*ones(n)

    elif _pars['SYNTH_OUT'] == 'generator':
        for i in range(n):
            yield A


def sweep_cosine(n, fs, f0, f1, A=1., kwargs=None):
    """
    Build a generator that yields a sweep sine between f0 and f1.

    Parameters
    ----------

    n : int
        Number of samples generated.

    fs : int
        Sample rate in Hz.

    f0 : float
        Initial frequency in Hz.

    f1 : float
        Final frequency in Hz such that f1>f0

    A : float, optional
        Amplitude (the default is 1.0).

    phi : float, optional
        original phase in degrees, default is -90 (sin chirp).

    method : {‘linear’, ‘quadratic’, ‘logarithmic’, ‘hyperbolic’}, optional
        Kind of frequency sweep. If not given, linear is assumed.

    Yields
    ------

    s : float
        Sequence of sweep values.

    See Also
    --------
    scipy.signal.chirp

    """
    if kwargs is None:
        kwargs = {}

    if 'phi' not in kwargs.keys():
        kwargs.update({'phi': -90})

    T = float(n-1)/float(fs)

    def mychirp(t):
        return A*chirp(t, f0=f0, f1=f1, t1=T, **kwargs)

    if _pars['SYNTH_OUT'] == 'array':
        return mychirp(linspace(0, T, n))

    elif _pars['SYNTH_OUT'] == 'generator':
        for t in linspace(0, T, n):
            yield mychirp(t)


def signalgenerator(**kwargs):
    """
    Return a generator that yields variety of signals.

    Parameters
    ----------
    which : str, optional
        Signal type (the default is 'zero'):
            * 'zero' yields zeros,
            * 'const' yields a constant value,
            * 'sin' yields a sine wave,
            * 'cos' yields a cosine wave,
            * 'noise' yields a random value from a uniform p.d.f,
            * 'sweep' yields a sine wave with increasing frequency,
            * 'step' yields a step function.

    tsig : float, optional
        single cycle duration (in seconds). The default is 1.

    ncycles : int, optional
        Number of cycles generated (the default is 1).

    tdeb : int, optional
        duration of sequence of 0.0 generated before the cycles  (in seconds).
        The default is 0.

    tend : int, optional
        duration of sequence of 0.0 generated after the cycles  (in seconds).
        The default is 0.

    fs : int, optional
        Sample rate in Hz (the default is 1000).

    A : float, optional
        Peak to peak amplitude (the default is 1.0).

    A1 : float, optional
        Amplitude of second sin wave in 'sin' mode only (the default is 1.0).

    f0 : float, optional
        Sin frequency (the default is 10.0Hz).

    f1 : float or None, optional
        Secondary frequency:
            * add a second sin wave in 'sin' mode,
            * set final frequency in 'sweep' mode.

    cycle_ratio : float, optional
        Cycle ratio between 0.0 and 1.0 (the default is 1.0) in reference \
to PWM.

    attack_ratio : float, optional
        Attack envelope ratio w.r.t. n*cycle_ratio (the default is 0.).

    decay_ratio : float, optional
        Decay envelope ratio w.r.t. n*cycle_ratio (the default is 0.).

    ramp_on : bool, optional
        Set the linear increasing of output during all cycles \
(the default is False).

    bkgrd_noise : float, optional
        Amplitude of an overall background noise from uniform p.d.f \
(the default is 0.0).

    Yields
    ------
    s : float
        signal value
    """

    parameters = build_parameters(**kwargs)

    def clamp_signal(x, xmin, xmax):
        cmax = npmax(vstack((x, xmin*ones_like(x))), axis=0)
        return npmin(vstack((cmax, xmax*ones_like(x))), axis=0)

    def ramp(i):
        if parameters['ramp_on']:
            return i/float(parameters['ncycles']*parameters['nsig']-1)
        else:
            return ones_like(i)

    def env(i):
        if parameters['nd'] > 0:
            enva = clamp_signal((parameters['non']-i)/float(parameters['nd']),
                                0, 1)
        else:
            enva = ones_like(i)
        if parameters['na'] > 0:
            envd = clamp_signal(i/float(parameters['na']), 0, 1)
        else:
            envd = ones_like(i)

        return enva * envd

    def background_noise(n=None):
        if n is None:
            if isinstance(parameters['bkgrd_noise'], (int, float)):
                return next(randomuniform(1, parameters['bkgrd_noise']))
            else:
                return 0.
        else:
            if isinstance(parameters['bkgrd_noise'], (int, float)):
                return randomuniform(n, parameters['bkgrd_noise'])
            else:
                return zeros(n)

    def array():
        # deb
        deb = background_noise(parameters['ndeb'])

        # cycles
        for c in range(parameters['ncycles']):
            if parameters['which'] == 'zero':
                Sig = constant(parameters['non'], 0.)
            elif parameters['which'] == 'const':
                Sig = constant(parameters['non'], parameters['A'])
            elif parameters['which'] == 'sin':
                Sig = sine(parameters['non'],
                           parameters['fs'],
                           f0=parameters['f0'],
                           f1=parameters['f1'],
                           A=parameters['A'],
                           A1=parameters['A1'])
            elif parameters['which'] == 'cos':
                Sig = cosine(parameters['non'],
                             parameters['fs'],
                             parameters['f0'],
                             parameters['A'])
            elif parameters['which'] == 'noise':
                Sig = randomuniform(parameters['non'],
                                    parameters['A'])
            elif parameters['which'] == 'step':
                Sig = constant(parameters['non'],
                               parameters['A'])
            elif parameters['which'] == 'sweep':
                Sig = sweep_cosine(parameters['non'],
                                   parameters['fs'],
                                   parameters['f0'],
                                   parameters['f1'],
                                   parameters['A'],
                                   parameters)
            else:
                print('Unknown synthesis method \
{0!s}.'.format(parameters['which']))
                raise NameError
            nsigc = Sig.shape[0]
            i = arange(nsigc)

            cycle_deb = ramp(i+c*parameters['nsig'])*env(i)*Sig + \
                background_noise(nsigc)

            cycle_end = background_noise(parameters['noff'])

        # end
        end = background_noise(parameters['nend'])

        return hstack((deb, cycle_deb, cycle_end, end))

    def generator():
        # deb
        for e in range(parameters['ndeb']):
            yield background_noise()

        # cycles
        for c in range(parameters['ncycles']):
            if parameters['which'] == 'zero':
                Sig = constant(parameters['non'], 0.)
            elif parameters['which'] == 'const':
                Sig = constant(parameters['non'], parameters['A'])
            elif parameters['which'] == 'sin':
                Sig = sine(parameters['non'],
                           parameters['fs'],
                           f0=parameters['f0'],
                           f1=parameters['f1'],
                           A=parameters['A'],
                           A1=parameters['A1'])
            elif parameters['which'] == 'cos':
                Sig = cosine(parameters['non'],
                             parameters['fs'],
                             parameters['f0'],
                             parameters['A'])
            elif parameters['which'] == 'noise':
                Sig = randomuniform(parameters['non'],
                                    parameters['A'])
            elif parameters['which'] == 'step':
                Sig = constant(parameters['non'],
                               parameters['A'])
            elif parameters['which'] == 'sweep':
                Sig = sweep_cosine(parameters['non'],
                                   parameters['fs'],
                                   parameters['f0'],
                                   parameters['f1'],
                                   parameters['A'],
                                   parameters)
            else:
                print('Unknown synthesis method \
{0!s}.'.format(parameters['which']))
                raise NameError
            i = 0
            for v in Sig:
                yield ramp(i+c*parameters['nsig'])*env(i)*v + \
                    background_noise()
                i += 1
            for i in range(parameters['noff']):
                yield background_noise()

        # end
        for i in range(parameters['nend']):
            yield background_noise()

    if _pars['SYNTH_OUT'] == 'array':
        return array()

    elif _pars['SYNTH_OUT'] == 'generator':
        return generator


def build_parameters(**kwargs):
    parameters = kwargs.copy()
    parameters.setdefault('which', 'sin')
    if not parameters['which'] in names:
        txt = 'Unknown synthesis method {0!s}.'.format(parameters['which'])
        raise NotImplementedError(txt)

    parameters.setdefault('tsig', 1.)
    parameters.setdefault('ncycles', 1)
    parameters.setdefault('tdeb', 0.)
    parameters.setdefault('tend', 0.)
    parameters.setdefault('fs', int(1e3))
    parameters.setdefault('A', 1.)
    parameters.setdefault('A1', 0.)
    parameters.setdefault('f0', 10.)
    parameters.setdefault('f1', 100.)
    parameters.setdefault('cycle_ratio', 1.)
    parameters.setdefault('attack_ratio', 0.)
    parameters.setdefault('decay_ratio', 0.)
    parameters.setdefault('ramp_on', False)
    parameters.setdefault('bkgrd_noise', 0.)

    parameters['nsig'] = int(parameters['tsig']*parameters['fs'])
    parameters['ndeb'] = int(parameters['tdeb']*parameters['fs'])
    parameters['nend'] = int(parameters['tend']*parameters['fs'])
    parameters['non'] = int(parameters['nsig']*parameters['cycle_ratio'])
    parameters['noff'] = parameters['nsig'] - parameters['non']

    parameters['na'], parameters['nd'] = (int(parameters['attack_ratio']*parameters['non']),
                                          int(parameters['decay_ratio']*parameters['non']))
    return parameters
