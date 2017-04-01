# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 18:57:05 2016

@author: Falaize
"""


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
    from numpy import sin, pi
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
    from numpy import cos, pi
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

    from numpy.random import uniform

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

    Yields
    ------
    s : float
        Sequence of sweep values.
    """
    if kwargs is None:
        kwargs = {}
    if 'phi' not in kwargs.keys():
        kwargs.update({'phi': -90})
    from numpy import linspace
    from scipy.signal import chirp
    T = float(n-1)/float(fs)
    for t in linspace(0, T, n):
        yield A*chirp(t, f0=f0, f1=f1, t1=T, **kwargs)


def signalgenerator(which='sin', tsig=1.,  ncycles=1, tdeb=0., tend=0.,
                    fs=int(1e3), A=1., A1=0., f0=10., f1=100., cycle_ratio=1.,
                    attack_ratio=0., decay_ratio=0., ramp_on=False, bkgrd_noise=0., kwargs=None):
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
    nsig = int(tsig*fs)
    ndeb = int(tdeb*fs)
    nend = int(tend*fs)
    non = int(nsig*cycle_ratio)
    noff = nsig - non

    na, nd = int(attack_ratio*non), int(decay_ratio*non)

    if kwargs is None:
        kwargs = {}

    def clamp_signal(x, xmin, xmax):
        clamp_below = max((x, xmin))
        return min((xmax, clamp_below))

    def ramp(i):
        return i/float(ncycles*nsig-1) if ramp_on else 1.

    def env(i):
        enva = clamp_signal((non-i)/float(nd), 0, 1) if nd > 0 else 1
        envd = clamp_signal(i/float(na), 0, 1) if na > 0 else 1
        return enva * envd

    def background_noise():
        if isinstance(bkgrd_noise, (int, float)):
            return next(randomuniform(1, bkgrd_noise))
        else:
            return 0.

    def generator():
        for i in range(ndeb):
            yield background_noise()
        for c in range(ncycles):
            if which == 'zero':
                Sig = constant(non, 0.)
            if which == 'const':
                Sig = constant(non, A)
            elif which == 'sin':
                Sig = sine(non, fs, f0=f0, f1=f1, A=A, A1=A1)
            elif which == 'cos':
                Sig = cosine(non, fs, f0, A)
            elif which == 'noise':
                Sig = randomuniform(non, A)
            elif which == 'step':
                Sig = constant(non, A)
            elif which == 'sweep':
                Sig = sweep_cosine(non, fs, f0, f1, A, kwargs)
            else:
                print('{0!s} unknown.'.format(which))
                raise NameError
            i = 0
            for v in Sig:
                yield ramp(i+c*nsig)*env(i)*v + background_noise()
                i += 1
            for i in range(noff):
                yield background_noise()
        for i in range(nend):
            yield background_noise()
    return generator


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


if __name__ is '__main__':
    fs = 100
    f0 = 1.
    Dur = 5.
    nt = int(Dur*fs)
    f1 = 10
    s = [el for el in signalgenerator(which='sweep', tsig=Dur, noisy=0.01,
                                      fs=fs, f0=f0, f1=f1, A=2, A1=-90)()]
    from waves import wavwrite
    wavwrite(s, fs, 'sweep', normalize=True)
    from matplotlib.pyplot import specgram, cm
    specgram(s, NFFT=2**10, cmap=cm.bone_r)
    from pyphs.plots.singleplots import singleplot
    t = [el/float(fs) for el in range(nt)]
    singleplot(t, (s, ))
