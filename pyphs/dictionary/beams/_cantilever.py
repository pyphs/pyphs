#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 20:11:16 2017

@author: Falaize
"""
from numpy import (sqrt, sin, cos, cosh, sinh, array, pi, linspace,
                   nonzero, diff, sign, newaxis)
from pyphs.dictionary.mechanics import Mass, Stiffness, Damper
from pyphs.dictionary.connectors import Transformer
from pyphs import Graph
from pyphs.graphs import datum


def parameters_JSV2016():
    pars = {
            # Fondamental frequency (Hz)
            'F': 440.,
            # [m] Radius of the cylinrical beam
            'R': 1*1e-3,
            # [#] Number of simulated eigen-modes
            'N': 5,
            # [s] Decay for the eigenmodes of the beam
            'A': 1e-2,
            # Coeficient for damping coefficient progression w.r.t wave number
            'D': 2,
            # [N/m**2] Young modulus of the Beam (steel = 180*1e9)
            'E': 180*1e9,
            # [kg/m**3] Mass density (steel = 7750)
            'M': 7750.,
    }

    return pars


def beamLength(f0, Kb, Mb):
    """
    Return the lengths L of a cylindrical cantilever beam with radius r, mass
    densisty m and Young's modulus E that corresponds to the fondamental
    frequency f0.

    Parameters
    ----------
    f0 : float
      Fondamental frequency of the vibrating cantilever beam (Hz)

    Mb : float
        Mass per unit-length

    Kb : float
        Flexural rigidity

    Returns
    -------
    Lb : float
      Return the length of the beam (m)

    """

    # [1/m] Wave Numer associated to the first eigen-mode
    #     k0**4 = (2*pi*f0)^2*Mb/Kb

    k0 = (((2*pi*f0)**2)*Mb/Kb)**(1./4.)
    # [m] A vector of Length
    Lb = linspace(0, 10, 10**7)
    # Add an axis to get L as a 2-dimensional array
    Lb = Lb[newaxis, :]
    # Index of length in L satisfying the eigen-modes cos(k*L)=-1./cosh(k*L)
    Indices = nonzero((abs(diff(sign(1+cosh(k0*Lb)*cos(k0*Lb))))).flatten())[0]
    # [m] Corresponding length in L
    return Lb[:, Indices[0]][0]


def waveNumbers(N, Lb, Kb, Mb):
    """
    Compute nk wavenumbers and eigen frequencies for a cylindrical cantilever
    beam with length L, flexural rigidity kappa and mass per unit length rho.

    km = (omegam^2*Mb/Kb)^(1/4)
    omegam = (km**4*Kb/Mb)**(1/2)

    Parameters
    ----------

    N : int
      Number of returned wavenumbers

    Lb : float
        Length of the cantilever beam (m)

    Kb : float
        Flexural rigidity  (N.m^2)

    Mb : float
     Mass per unit length (kg.m^-1)

    Relations
    ---------

    cosh(km*L)*cos(km*L) + 1 = 0

    fn = sqrt(kappa/rho) * k**2 / (2*pi)

    Returns
    -------

    k : list of floats
      List of nk wavenumbers (1/m)

    fk : list of floats
      List of nk eigen frequencies (Hz)

    """
    nPeriods = N
    nPoints = N*1e6
    # [1/m] A vector of wavenumners
    k = linspace(0., nPeriods*2*pi/Lb, int(nPoints))
    # Add an axis to get k as a 2-dimensional array
    k = k[newaxis, :]
    # Indices of wavenumers in k satisfying eigen-modes cos(k*L)=-1./cosh(k*L)
    Indices = nonzero((abs(diff(sign(1+ cosh(k*Lb)*cos(k*Lb))))).flatten())[0]
    # [m] Corresponding wavenumners in k
    k = k[:, Indices]
    # [Hz] Frequencies associated to k
    fk = sqrt((k**4)*Kb/Mb)/(2*pi)
    return k[0][:N], fk[0][:N]


def omega_cosine(zp, wp, Lb, k):
    """

    coefficients associated with the projection of a contact distributed
    according to a cosine function centered at zp with zeros outside the
    interval (zp-wp/2, zp+wp/2) over the modes (wavenumbers) k.

    Parameters
    ----------

    zp : float
        Position of the contact (m).

    wp : float
        Width of the contact (m).

    Lb : float
        Length of the beam (m).

    k : list of floats
        List of wave numbers (1/m).

    Return
    -------

    omega : list of floats
        List of M coefficients associated with the projection of a contact
        distributed according to a cosine function centered at zp with zeros
        outside the interval (zp-wp/2, zp+wp/2) over the mode (wavenumber) km.
        Fm = omega[m]*Fext.
    """

    km = array(k)
    a = (sqrt(2)*pi**2*(cosh(km*Lb)*((pi**2+(km*wp)**2)*cos((km*wp)/2)*cos(km*zp)-(pi**2-(km*wp)**2)*cosh((km*wp)/2)*cosh(km*zp)) + (pi**2 + (km*wp)**2)*cos((km*wp)/2)*(cos(km*(Lb-zp))-sin(km*zp)*sinh(km*Lb))-(pi**2-(km*wp)**2)*cosh((km*wp)/2)*(cos(km*Lb)*cosh(km*zp)+(sin(km*Lb)-sinh(km*Lb))*sinh(km*zp))))
    b = ((pi**4-(km*wp)**4)*sqrt(-(1/km)*(-km*Lb*(2 + cos(2*km*Lb) + cosh(2*km*Lb)) + 2*cosh(km*Lb)*(-2*km*Lb*cos(km*Lb)+sin(km*Lb))+cosh(km*Lb)**2*sin(2*km*Lb) + 2*cos(km*Lb)*sinh(km*Lb)+(cos(km*Lb)**2)*sinh(2*km*Lb))))
    omega = list(a/b)
    return omega


class Cantilever(Graph):
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
        * 'F': [Hz] Fondamental frequency (440.),
        * 'R': [m] Radius of the cylinrical beam (1*1e-3),
        * 'N': [d.u] Number of simulated eigen-modes (5),
        * 'A': [s] Decay for the eigenmodes of the beam (9e-3),
        * 'D': [d.u] damping progression w.r.t wave number (6.),
        * 'E': [N/m**2] Young modulus of the Beam (steel = 180*1e9),
        * 'M': [kg/m**3] Mass density (steel = 7750),
        * 'z#': [0-1] relative position of contact # w.r.t. beam length (0.15),
        * 'w#': [m] width of contact # with the beam (1.5cm), if 0 a point
            contact is assumed.
    """
    def __init__(self, label, nodes, **kwargs):

        pars = parameters_JSV2016()

        for k in kwargs.keys():
            if k not in pars.keys() and str(k)[0] not in 'zw':
                raise AttributeError('parameter {} unknown'.format(k))

        Graph.__init__(self, label=label)

        pars.update(kwargs)
        pars.update({
                     # [kg] Modal mass density
                    'Mb': pi*(pars['R']**2)*pars['M'],
                    # [N/m] Modal stiffness
                    'Kb': (pars['E']*pi*pars['R']**4.)/4.,
                    })
        pars.update({
                    # [m] Tine length for the fondamental frequency f0[Hz]
                    'Lb': beamLength(pars['F'], pars['Kb'], pars['Mb'])
                    })

        # [1/m] list of the nkmax first cantilever beam  modes with length L
        k, fk = waveNumbers(pars['N'], pars['Lb'], pars['Kb'], pars['Mb'])

        # truncate below the Nyquist frequency fe/2
        # list of the nk first modes below the Nyquist frequency fe/2 [1/m]
        # k = k[(fk < pars['n']/2).nonzero()]
        # list of the nk first frequencies below the Nyquist frequency fe/2 [Hz]
        # fk = fk[(fk < pars['fs']/2).nonzero()]

        # [#] number of simulated modes
        pars.update({'kmodes': k,
                     'fmodes': fk})
        pars['N'] = len(pars['kmodes'])

        # [N/m**1] Modal damping coefficient
        pars.update({'Ab_array': pars['A']*10**(linspace(0, pars['D'],
                                                         pars['N']))})
        # definition of stiffnesses values
        coeffs = pars['Kb']*(k.flatten()**4)
        # definition of stiffnesses components
        for i, c in enumerate(coeffs):
            stiffness = Stiffness(label+'K'+str(i),
                                  (datum, label+'M'+str(i)),
                                  K=(label+'K'+str(i), c))
            self += stiffness
        # definition of masses values
        coeffs = [pars['Mb']]*pars['N']
        # definition of masses components
        for i, c in enumerate(coeffs):
            mass = Mass(label+'M'+str(i),
                        (label+'M'+str(i), ),
                        M=(label+'M'+str(i), c))
            self += mass

        # definition of dampers components
        coeffs = list(pars['Ab_array'])
        # definition of dampers components
        for i, c in enumerate(coeffs):
            damper = Damper(label+'A'+str(i),
                            (datum, label+'M'+str(i)),
                            A=(label+'A'+str(i), c))
            self += damper

        for n, Nn in enumerate(nodes):

            label_n = label+'T'+str(n)
            Omega = omega_cosine(pars['z'+str(n+1)]*pars['Lb'],
                                 pars['w'+str(n+1)],
                                 pars['Lb'], pars['kmodes'])

            # transformers associated with the coefficients of modal projection

            # Begining of the serial connection of transformers primals
            A1 = Nn
            # tail node for the serial connection of transformers primals
            if pars['N'] == 1:
                A2 = datum
            else:
                A2 = label_n + str(0)

            # iterate over coefficients values
            for i, o in enumerate(Omega):

                # define transfomer
                transfo = Transformer(label_n+str(i),
                                      (A1, A2,
                                      datum, label+'M'+str(i)),
                                      alpha=(label_n+'alpha'+str(i), o))
                self += transfo

                # update nodes
                A1 = label_n+str(i)
                if i == pars['N']-2:
                    A2 = datum
                else:
                    A2 = label_n+str(i+1)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'F': 440.,
                              'R': 1*1e-3,
                              'N': 5,
                              'A': 1e-2,
                              'D': 0.,
                              'E': 180*1e9,
                              'M': 7750,
                              'z1': 0.15,
                              'w1': 1.5e-2,
                              'z2': 1,
                              'w2': 0.}
                              }
