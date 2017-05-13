#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 20:11:16 2017

@author: Falaize
"""
import sympy as sp
from numpy import (sqrt, sin, cos, tanh, cosh, sinh, array, pi, linspace,
                   nonzero, diff, sign, newaxis)
from pyphs.dictionary.mechanics import Mass, Stiffness, Damper, datum
from pyphs.dictionary.connectors import Transformer
from pyphs import PHSGraph


def parameters_JSV2016():
    pars = {
            # Fondamental frequency (Hz)
            'f0': 440.,
            # [m] Radius of the cylinrical beam
            'r': 1*1e-3,
            # [#] Number of simulated eigen-modes
            'nk': 5,
            # [s] Decay for the eigenmodes of the beam
            'alpha': 1e-2,
            # Coeficient for damping coefficient progression w.r.t wave number
            'damping': 0,
            # [N/m**2] Young modulus of the Beam (steel = 180*1e9)
            'E': 180*1e9,
            # [kg/m**3] Mass density (steel = 7750)
            'm': 7750.,
            # [0,1] relative position of the hammer w.r.t. the beam length L
            'zh': 0.15,
            # [m] width of the contact with the beam
            'wh': 1.5*1e-2,
    }

    pars.update({
                 # [kg] Modal mass density
                'rho': pars['m']*pi*pars['r']**2.,
                # [N/m] Modal stiffness
                'kappa': pars['E']*pi*pars['r']**4/4.,
                })
    return pars


def omega_point(kmodes, L, z):
    """

    Coefficients of modal projection of a single point located at `z` over the
    modes of a cantilever beam with lengt `L` and wave numbers `kmodes`.

    Parameters
    ----------

    kmodes : list of float
      Wavenumber (m^-1)

    L : float
        Length of the tine (m)

    z : float
        position along the tine (m)

    Return
    -------

    omega : list of floats
        List of coefficient for the projection on mode m:
        Fm = omega[m]*Fext.

    """

    km = array(kmodes)
    a = (sqrt(2)*(sin(km*L)*(sin(km*z) - sinh(km * z)) -
         sinh(km * (L - z))*tanh(km * L) +
       sinh(km*L)*(-sin(km*z) + cos(km * z)*tanh(km * L))))
    c = (2.*sin(km*L) + cosh(km*L)*sin(2*km*L))
    d = km*L*(-2 + cos(2*km*L))
    f = km*L*cosh(2*km*L)
    b = (d + f - cosh(km*L)*c)/km
    return a/sqrt(b)


def beamLength(f0, r, m, E):
    """
    Return the lengths L of a cylindrical beam with radius r, mass densisty m
    and Young's modulus E that corresponds to the fondamental frequency f0

    Parameters
    ----------
    f0 : float
      Fondamental frequency of the vibrating cantilever beam (Hz)

    r : float
        Radius of the beam (m)

    m : float
        Volumetric densisty of mass for the chosen material of the
        beam (kg/m**3)

    E : float
        Young's modulus for the chosen material of the beam (N/m**2)

    Returns
    -------
    L : float
      Return the length of the beam (m)

    """

    # [m**2] Area of the cross section of the beam
    A = pi*r**2
    # [m**4] Moment of inertia of plane area for a section of the beam
    I = pi*r**4/4.
    # [1/m] Wave Numer associated to the first eigen-mode
    k = sqrt(2*pi*sqrt(m*A/(E*I))*f0)
    # [m] A vector of Length
    L = linspace(0, 1, 10**7)
    # Add an axis to get L as a 2-dimensional array
    L = L[newaxis, :]
    # Index of length in L satisfying the eigen-modes cos(k*L)=-1./cosh(k*L)
    Indexes = nonzero((abs(diff(sign(-1./cosh(k*L)-cos(k*L))))).flatten())[0]
    # [m] Corresponding length in L
    return L[:, Indexes[0]][0]


def waveNumbers(nk, L, kappa, rho):
    """
    Compute nk wavenumbers and eigen frequencies for a cylindrical tine with
    length L, flexural rigidity kappa and mass per unit length rho (kg.m^-1).

    Parameters
    ----------

    nk : int
      Number of returned wavenumbers

    L : float
        Length of the tine (m)

    kappa : float
        Linear stiffness (flexural rigidity, N.m^2)

    Relations
    --------

    cosh(km*L)*cos(km*L) + 1 = 0

    km = (2*pi*f*rho/kappa)

    Returns
    -------

    k : list of floats
      List of nk wavenumbers (1/m)

    fk : list of floats
      List of nk eigen frequencies (Hz)

    """
    nPeriods = nk/2.
    nPoints = nk*1e6
    # [1/m] A vector of wavenumners
    k = linspace(0, nPeriods*2*pi/L, nPoints)
    # Add an axis to get k as a 2-dimensional array
    k = k[newaxis, :]
    # Index of wavenumers in k satisfying eigen-modes cos(k*L)=-1./cosh(k*L)
    Indexes = nonzero((abs(diff(sign(-1./cosh(k*L)-cos(k*L))))).flatten())[0]
    # [m] Corresponding wavenumners in k
    k = k[:, Indexes]
    # [Hz] Frequencies associated to k
    fk = (1./(2*pi))*sqrt(kappa/rho)*k**2
    return k, fk


def omega_const(pars):
    """

    Coefficients of modal projection of a single point located at `z` over the
    modes of a cantilever beam with lengt `L` and wave numbers `kmodes`.

    Parameters
    ----------

    kmodes : list of float
      Wavenumber (m^-1)

    L : float
        Length of the tine (m)

    z : float
        position along the tine (m)

    Return
    -------

    omega : list of floats
        List of coefficient for the projection on mode m:
        Fm = omega[m]*Fext.

    """
    omega = []
    wh = pars['wh']
    L = pars['L']
    zh = pars['zh']
    for n in range(pars['nk']):
        kn = pars['kmodes'][n]
        kl = kn*pars['L']
        term1 = sp.sqrt(2)*(2*sp.sin((kn*wh)/2)*(sp.cos(kn*(L-zh))+sp.cos(kn*zh)*sp.cosh(kl)-sp.sin(kn*zh)*sp.sinh(kl))-2*sp.sinh((kn*wh)/2)*(sp.cosh(kn*(L-zh))+sp.cos(kl)*sp.cosh(kn*zh)+sp.sin(kl)*sp.sinh(kn*zh)))
        term2 = sp.sqrt(kn)*sp.sqrt(kl*(-2+sp.cos(2*kl))+kl*sp.cosh(2*kl)-sp.cosh(kl)*(2*sp.sin(kl)+sp.cosh(kl)*sp.sin(2*kl)))
        omega.append(term1/term2)
    omega = sp.Matrix(omega)
    return omega


class Cantilever(PHSGraph):
    """
    Cantilever Beam
    ================
    Euler-Bernouilli cantilever Beam

    Parameters
    -----------

    label: str
        Cantilever beam label.

    nodes : (N1, )
        Node for connection to an e-control port.

    kwargs : dictionary with following "key: value" (default in parenthesis)
        * 'f0': [Hz] Fondamental frequency (440.),
        * 'r': [m] Radius of the cylinrical beam (1*1e-3),
        * 'nk': [d.u] Number of simulated eigen-modes (5),
        * 'alpha': [s] Decay for the eigenmodes of the beam (9e-3),
        * 'damping': [d.u] damping progression w.r.t wave number (6.),
        * 'E': [N/m**2] Young modulus of the Beam (steel = 180*1e9),
        * 'm': [kg/m**3] Mass density (steel = 7750),
        * 'zh': [0-1] relative position of contact w.r.t. beam length (0.15),
        * 'wh': [m] width of the contact with the beam (1.5cm),
    """
    def __init__(self, label, nodes, **kwargs):
        pars = parameters_JSV2016()
        pars.update(kwargs)
        PHSGraph.__init__(self, label=label)
        # [m] Tine length for the fondamental frequency f0[Hz]
        L = beamLength(pars['f0'], pars['r'], pars['m'], pars['E'])
        pars.update({'L': L})
        # [1/m] list of the nkmax first cantilever beam  modes with length L
        k, fk = waveNumbers(pars['nk'], L, pars['kappa'], pars['rho'])

        # truncate below the Nyquist frequency fe/2
        # list of the nk first modes below the Nyquist frequency fe/2 [1/m]
        # k = k[(fk < pars['n']/2).nonzero()]
        # list of the nk first frequencies below the Nyquist frequency fe/2 [Hz]
        # fk = fk[(fk < pars['fs']/2).nonzero()]

        # [#] number of simulated modes
        pars.update({'kmodes': k[0],
                     'fmodes': fk[0]})
        # [N/m**1] Modal damping coefficient
        a = pars['alpha']
        dp = pars['damping']
        pars.update({'alpha': a*10**(linspace(0, dp, pars['nk']))})
        # Spatial distributions
        # HAMMER
        # [m] position of the hammer
        zh = pars['wh']/2. + pars['zh']*(L-pars['wh'])
        pars.update({'zh': zh})
        # definition of stiffnesses values
        ka = pars['kappa']
        coeffs = ka*(k.flatten()**4)
        # definition of stiffnesses components
        for i, c in enumerate(coeffs):
            stiffness = Stiffness(label+'K'+str(i),
                                  (datum, label+'M'+str(i)),
                                  K=(label+'K'+str(i), c))
            self += stiffness
        # definition of masses values
        coeffs = [pars['rho']]*pars['nk']
        # definition of masses components
        for i, c in enumerate(coeffs):
            mass = Mass(label+'M'+str(i),
                        (label+'M'+str(i), ),
                        M=(label+'M'+str(i), c))
            self += mass

        # definition of dampers components
        coeffs = list(pars['alpha'])
        # definition of dampers components
        for i, c in enumerate(coeffs):
            damper = Damper(label+'A'+str(i),
                            (datum, label+'M'+str(i)),
                            A=(label+'A'+str(i), c))
            self += damper
        Omega = omega_const(pars)

        # transformers associated with the coefficients of modal projection
        A1 = nodes[0]  # system node
        # tail node for the serial connection of transformers primals
        if pars['nk'] == 1:
            A2 = datum
        else:
            A2 = label+'T'+str(0)
        # iterate over coefficients values
        for i, o in enumerate(Omega):

            # define transfomer
            transfo = Transformer(label+'T'+str(i),
                                  (A1, A2,
                                  datum, label+'M'+str(i)),
                                  alpha=(label+'alpha'+str(i), (o)))
            self += transfo

            # update nodes
            A1 = label+'T'+str(i)
            if i == pars['nk']-2:
                A2 = datum
            else:
                A2 = label+'T'+str(i+1)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', ),
                'arguments': {'f0': 440.,
                              'r': 1*1e-3,
                              'nk': 5,
                              'alpha': 1e-2,
                              'damping': 0.,
                              'E': 180*1e9,
                              'm': 7750,
                              'zh': 0.15,
                              'wh': 1.5e-2}}
