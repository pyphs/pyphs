# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:31:24 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import numpy as np

from pyphs import PHSGraph
from pyphs.config import EPS

from .edges import PHSDissipativeLinear, PHSStorageLinear
from pyphs.dictionary.connectors import Transformer

__all__ = ['Fracinte']

class Fracdere(PHSGraph):
    """ Fractional Effort Controlled springpot element
    usgae: FracDerEffortCtrl label ['n1','n2'] [rAlphaMag, alphaMag ,NbPoles]

    """
    def __init__(self, label, nodes, **kwargs):
        PHSGraph.__init__(self, label)
        if 'p' not in kwargs:
            p = 1
        else:
            p = kwargs.pop('p')

        if 'alpha' not in kwargs:
            alpha = 0.5
        else:
            alpha = kwargs.pop('alpha')

        diagRmu, diagQmu = fractionalDifferenciatorWeights(p, alpha, **kwargs)

        # Truncation of poles with null Q
        nbPoles = diagRmu.__len__()

        datum = self.graph.netlist.datum
        for n in range(nbPoles):

            Rn = diagRmu[n]**(-1)  # here, diagRmu[n] is a conductance (e-ctrl)
            Ndeb = nodes[0]
            N1 = 'N'+label+str(n)+"_2"
            self += PHSDissipativeLinear(label+'R'+str(n),
                                         (Ndeb, N1),
                                         coeff=Rn)

            Qn = diagQmu[n]
            N2 = 'N'+label+str(n)+"_2"
            self += PHSStorageLinear(label+'Q'+str(n),
                                     (N2, datum),
                                     coeff=Qn,
                                     inv_coeff=True)

            Nend = nodes[1]
            self += Transformer(label+'alpha'+str(n),
                                (N1, Nend, N2, datum),
                                alpha=diagRmu[n]**-1)


class Fracderf(PHSGraph):
    """ Fractional Flux Controlled storage element
    usgae: FracIntEffortCtrl label ['n1','n2'] [rAlphaMag, alphaMag ,NbPoles, \
(fmin, fmax)]
    """
    def __init__(self, label, nodes, **kwargs):
        PHSGraph.__init__(self, label)
        if 'p' not in kwargs:
            p = 1
        else:
            p = kwargs.pop('p')

        if 'alpha' not in kwargs:
            alpha = 0.5
        else:
            alpha = kwargs.pop('alpha')

        diagRmu, diagQmu = fractionalDifferenciatorWeights(p, alpha, **kwargs)

        # Truncation of poles with null Q
        nbPoles = diagRmu.__len__()

        datum = self.graph.netlist.datum
        for n in range(nbPoles):

            Rn = diagRmu[n]  # here, diagRmu[n] is a res (flux-controlled)
            Ndeb = nodes[0]
            N1 = 'N'+label+str(n)+"_2"
            self += PHSDissipativeLinear(label+'R'+str(n),
                                         (Ndeb, N1),
                                         coeff=Rn)

            Qn = diagQmu[n]
            N2 = 'N'+label+str(n)+"_2"
            self += PHSStorageLinear(label+'Q'+str(n),
                                     (N2, datum),
                                     coeff=Qn,
                                     inv_coeff=True)

            Nend = nodes[1]
            self += Transformer(label+'alpha'+str(n),
                                (Ndeb, Nend, N2, datum),
                                alpha=diagRmu[n]**-1)


def Fracinte(PHSGraph):
    """
Effort-controlled fractional integrator:
    f(s) = p * s^(-beta) * e(s)

Usage:
    fraccalc.Int_e(('n1','n2'): p=1; beta=0.5; NbPoles=10; \
OptimPolesMinMax=(-10,10); NbFreqPoints=200; OptimFreqsMinMax=(1, 48e3); \
DoPlot=False;)
    """
    def __init__(self, label, nodes, **kwargs):
        PHSGraph.__init__(self, label=label)

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
            temp_phs = PHSDissipativeLinear('R_'+label+str(n),
                                            (Ncomp, Nend),
                                            coeff=Rn)
            self += temp_phs

            Qn = diagQmu[n]
            Ndeb = nodes[0]
            temp_phs = PHSStorageLinear(label+str(n),
                                        (Ndeb, Ncomp),
                                        value=Qn,
                                        name='pL_',
                                        inv_coeff=True)
            self += temp_phs

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'p': 1,
                              'beta': 0.5,
                              'NbPoles': 20,
                              'PolesMinMax': (-5, 10),
                              'NbFreqPoints': 200,
                              'FreqsMinMax': (1, 48e3)}}


class Fracintf(PHSGraph):
    """ Fractional Flux Controlled storage element
    usgae: FracIntFluxCtrl label ['n1','n2'] [rAlphaMag, alphaMag ,NbPoles]

    """
    def __init__(self, label, nodes, **kwargs):
        PHSGraph.__init__(self, label)
        if 'p' not in kwargs:
            p = 1
        else:
            p = kwargs.pop('p')

        if 'alpha' not in kwargs:
            alpha = 0.5
        else:
            alpha = kwargs.pop('alpha')

        diagRmu, diagQmu = fractionalIntegratorWeights(p, alpha, **kwargs)

        # Truncation of poles with null Q
        nbPoles = diagRmu.__len__()

        Ndeb = nodes.pop()
        Nend = nodes[-1]
        for n in range(nbPoles):
            # here, diagRmu[n] is a resistance (flux-controlled)
            Rn = diagRmu[n]
            self += PHSDissipativeLinear(label + 'R' + str(n),
                                         (Ndeb, Nend),
                                         coeff=Rn)

            Qn = diagQmu[n]
            Ndeb = nodes[0]
            self += PHSStorageLinear(label + 'Q' + str(n),
                                     (Ndeb, Nend),
                                     coeff=Qn,
                                     inv_coeff=True)


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
            pn = p*Mu[n]**-1
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
        v3 = map(lambda x, y: x-y, v1, v2)
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


def fractionalDifferenciatorWeights(p, alpha, NbPoles=20,
                                    PolesMinMax=(-5, 10),
                                    NbFreqPoints=200,
                                    FreqsMinMax=(1, 48e3), DoPlot=True):

    # Defintion of the frequency grid
    fmin, fmax = FreqsMinMax
    wmin, wmax = 2*np.pi*fmin, 2*np.pi*fmax
    w = np.exp(np.log(wmin) +
               np.linspace(0, 1, NbFreqPoints+1)*np.log(wmax/wmin))
    w12 = np.sqrt(w[1:]*w[:-1])

    # Unpack min and max exponents to define the list of poles
    emin, emax = PolesMinMax
    Xi = np.logspace(emin, emax, NbPoles)  # xi_0 -> xi_{N+1}

    # Input to Output transfer function of the fractional integrator of
    # order 1-alpha
    beta = 1.-alpha

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
            diagR.append(p*Mu[n])
            diagQ.append(p*Mu[n]*Xi[n])

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
        v3 = map(lambda x, y: x-y, v1, v2)
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
