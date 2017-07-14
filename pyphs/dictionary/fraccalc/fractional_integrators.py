#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 17:57:10 2017

@author: Falaize
"""

from pyphs import Graph
import numpy as np
from pyphs.dictionary.edges import DissipativeLinear, StorageLinear
from pyphs.config import EPS



# ======================================================================= #


class Fracintec(Graph):
    """
Effort-controlled fractional integrator:
.. math:: f(s) = p \\, s^{-\\beta}  \\, e(s)

Usage
-----

.. code:: fraccalc.fracintec label ('n1','n2'): p=1; beta=0.5; NbPoles=10; \
PolesMinMax=(-10,10); NbFreqPoints=200; FreqsMinMax=(1, 48e3); \
DoPlot=False;
    """
    def __init__(self, label, nodes, **kwargs):
        Graph.__init__(self, label=label)

        if 'p' not in kwargs:
            p = 1
        else:
            p = kwargs.pop('p')

        if 'beta' not in kwargs:
            beta = 0.5
        else:
            beta = kwargs.pop('beta')

        self.core.subs.update({self.core.symbols('p_'+label): p,
                               self.core.symbols('beta_'+label): beta})

        diagRmu, diagQmu = fractionalIntegratorWeights(p, beta, **kwargs)

        # Truncation of poles with null Q
        nbPoles = diagRmu.__len__()

        for n in range(nbPoles):
            Rn = diagRmu[n]  # here, diagRmu[n] is a resistance (f-ctrl)
            Nend = nodes[1]
            Ncomp = 'iN_'+label + str(n)
            comp = DissipativeLinear('R_'+label+str(n),
                                            (Ncomp, Nend),
                                            coeff=Rn,
                                            ctrl='f')
            self += comp

            Qn = diagQmu[n]
            Ndeb = nodes[0]
            comp = StorageLinear(label+str(n),
                                        (Ndeb, Ncomp),
                                        value=Qn,
                                        name='pL_',
                                        inv_coeff=False,
                                        ctrl='e')
            self += comp

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'p': 1.,
                              'beta': 0.5,
                              'NbPoles': 20,
                              'PolesMinMax': (-5, 10),
                              'NbFreqPoints': 200,
                              'FreqsMinMax': (1, 48e3)}}


# ======================================================================= #


class Fracintfc(Graph):
    """ 
Flux-controlled fractional integrator:
.. math:: e(s) = p \\, s^{-\\beta}  \\, f(s)

Usage
-----

.. code:: fraccalc.fracintfc label ('n1','n2'): p=1; beta=0.5; NbPoles=10; \
PolesMinMax=(-10,10); NbFreqPoints=200; FreqsMinMax=(1, 48e3); \
DoPlot=False;
    """
    def __init__(self, label, nodes, **kwargs):
        Graph.__init__(self, label=label)
        if 'p' not in kwargs:
            p = 1
        else:
            p = kwargs.pop('p')

        if 'beta' not in kwargs:
            beta = 0.5
        else:
            beta = kwargs.pop('beta')

        diagR, diagQ = fractionalIntegratorWeights(p, beta, **kwargs)

        # Truncation of poles with null Q
        nbPoles = diagR.__len__()

        N, Nend = nodes
        for n in range(nbPoles):
            if n < nbPoles-1:
                Ncomp = 'iN_'+label + str(n) + 'to' + str(n+1)
            else:
                Ncomp = Nend
            nodes = (N, Ncomp)
            # here, diagRmu[n] is a conductance (effort-controlled)
            Rn = diagR[n]
            self += DissipativeLinear(label + 'R' + str(n),
                                         nodes,
                                         coeff=Rn,
                                         inv_coeff=True,
                                         ctrl='e')

            Qn = diagQ[n]
            self += StorageLinear(label + 'Q' + str(n),
                                     nodes,
                                     value=Qn,
                                     inv_coeff=False,
                                     ctrl='f')
            N = Ncomp
    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'p': 1.,
                              'beta': 0.5,
                              'NbPoles': 20,
                              'PolesMinMax': (-5, 10),
                              'NbFreqPoints': 200,
                              'FreqsMinMax': (1, 48e3)}}


# ======================================================================= #


def fractionalIntegratorWeights(p, beta, NbPoles=10,
                                PolesMinMax=(-10, 10),
                                NbFreqPoints=200,
                                FreqsMinMax=(1, 48e3),
                                DoPlot=False):
    # Defintion of the frequency grid
    fmin, fmax = FreqsMinMax
    wmin, wmax = 2*np.pi*fmin, 2*np.pi*fmax
    w = np.exp(np.log(wmin) +
               np.linspace(0, 1, NbFreqPoints+1)*np.log(wmax/wmin))
    w12 = np.sqrt(w[1:]*w[:-1])

    # Unpack min and max exponents to define the list of poles
    emin, emax = PolesMinMax
    Xi = np.logspace(emin, emax, NbPoles)  # xi_0 -> xi_{N+1}

    # Input to Output transfer function of the fractional integrator
    def transferFunctionFracInt(s):
        return s**-beta

    # Target transfer function evaluated on the frequency grid
    T = transferFunctionFracInt(1j*w12)

    # Return the basis vector of elementary damping with poles Xi
    def Basis(s, Xi):
        return (s+Xi)**-1

    # Matrix of basis transfer function for each poles on the frequency grid
    M = np.zeros((NbFreqPoints, NbPoles), dtype=np.complex64)
    for k in np.arange(NbFreqPoints):
        M[k, :] = Basis(1j*w12[k], Xi)

    # Perceptual weights
    WBuildingVector = (np.log(w[1:])-np.log(w[:-1]))/(np.abs(T)**2)
    W = np.diagflat(WBuildingVector)

    # Definition of the cost function
    def CostFunction(mu):
        mat = np.dot(M, mu) - T
        cost = np.dot(np.conjugate(mat.T), np.dot(W, mat))
        return cost.real

    # Optimization constraints
    bnds = [(0, None) for n in range(NbPoles)]

    # Optimization
    from scipy.optimize import minimize
    MuOpt = minimize(CostFunction, np.ones(NbPoles), bounds=bnds, tol=EPS)
    Mu = MuOpt.x  # Get the solution

    # Conversion to phs parameters
    diagQ = []
    diagR = []

    # Eliminate 0 valued weigths
    for n in np.arange(NbPoles):
        if Mu[n] > 0:
            pn = (p*Mu[n])**-1
            diagR.append(pn*Xi[n])
            diagQ.append(pn**-1)

    if DoPlot:
        from matplotlib.pyplot import (figure, subplot, plot, semilogx, ylabel,
                                       legend, grid, xlabel)
        TOpt = np.array(M*np.matrix(Mu).T)
        wmin, wmax = 2*np.pi*fmin, 2*np.pi*fmax
        figure()
        subplot(2, 1, 1)
        faxis = w12[(wmin < w12) & (w12 < wmax)]/(2*np.pi)
        v1 = 20*np.log10(np.abs(T[(wmin < w12) & (w12 < wmax)]))
        v2 = 20*np.log10(np.abs(TOpt[(wmin < w12) & (w12 < wmax)]))
        v3 = list(map(lambda x, y: x-y, v1, v2))
        semilogx(faxis, v1, label='Target')
        semilogx(faxis, v2, label='Approx')
        ylabel('Transfert (dB)')
        legend(loc=0)
        grid()
        subplot(2, 1, 2)
        plot(faxis, v3, label='Error')
        xlabel('Log-frequencies (log Hz)')
        ylabel('Error (dB)')
        legend(loc=0)
        grid()

    return diagR, diagQ

