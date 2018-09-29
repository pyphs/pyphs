#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 18:00:15 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import numpy as np

from pyphs import Graph
from pyphs.config import EPS

from ..edges import DissipativeLinear, StorageLinear
from pyphs.dictionary.connectors import Transformer
from pyphs.graphs import datum
from pyphs.misc.rst import equation
from ..tools import componentDoc, parametersDefault
from ..fraccalc import metadata as dicmetadata


# ======================================================================= #


class Fracderec(Graph):

    def __init__(self, label, nodes, **kwargs):

        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        Graph.__init__(self, label=label)

        g = parameters.pop('g')
        alpha = parameters.pop('alpha')

        diagR, diagQ = fractionalDifferenciatorWeights(g, alpha, **parameters)

        # Truncation of poles with null Q
        nbPoles = diagR.__len__()

        Ndeb, Nend = nodes
        for n in range(nbPoles):

            Rn = diagR[n]  # here, diagR[n] is a conductance (e-ctrl)

            N1 = 'N'+label+str(n)+"_1"
            N2 = 'N'+label+str(n)+"_2"
            self += DissipativeLinear(label+'R'+str(n),
                                         (N1, Ndeb),
                                         inv_coeff=True,
                                         coeff=Rn,
                                         ctrl='e')



            Qn = diagQ[n]
            self += StorageLinear(label+'Q'+str(n),
                                     (N2, datum),
                                     value=Qn,
                                     ctrl='f',
                                     inv_coeff=False)

            self += Transformer(label+'alpha'+str(n),
                                (N1, Nend, N2, datum),
                                alpha=Rn**-1)

    metadata = {'title': 'Effort-controlled fractional derivator',
                'component': 'Fracderec',
                'label': 'fracder',
                'dico': 'fraccalc',
                'desc': r'Effort-controlled fractional derivator from [1]_ (chap 7):'+ equation(r'f(s) = g \, s^{alpha}  \, e(s).'),
                'nodesdesc': "Component terminals with positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameters',
                'parameters': [['g', "Gain", 'unknown', 1.],
                               ['alpha', "Derivation order in (0, 1)", 'd.u.', 0.5],
                               ['NbPoles', "Approximation order", 'd.u.', 20],
                               ['PolesMinMax', "Poles modules in :math:`(10^{min}, 10^{max})`", 'Hz', (-5, 10)],
                               ['NbFreqPoints', "Number of optimization points", 'd.u.', 200],
                               ['FreqsMinMax', "Optimization interval", 'Hz', (1, 48e3)],
                               ['DoPlot', "Plot transfer function", 'bool', False]],
                'refs': {1: "Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016."},
                'nnodes': 37,
                'nedges': 68,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }
    # Write documentation
    __doc__ = componentDoc(metadata)

# ======================================================================= #


class Fracderfc(Graph):
    def __init__(self, label, nodes, **kwargs):
        Graph.__init__(self, label=label)

        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        g = parameters.pop('g')
        alpha = parameters.pop('alpha')

        diagR, diagQ = fractionalDifferenciatorWeights(g, alpha, **parameters)

        # Truncation of poles with null Q
        nbPoles = diagR.__len__()

        Ndeb, Nend = nodes
        N1 = Ndeb
        for n in range(nbPoles):
            if n < nbPoles-1:
                N2 = 'N'+label+str(n)+"_1"
            else:
                N2 = Nend
            Rn = diagR[n]  # here, diagR[n] is a res (flux-controlled)
            self += DissipativeLinear(label+'R'+str(n),
                                         (N2, N1),
                                         ctrl='f',
                                         coeff=Rn,
                                         inv_coef=False)

            Qn = diagQ[n]
            N3 = 'N'+label+str(n)+"_2"
            self += StorageLinear(label+'Q'+str(n),
                                     (N3, datum),
                                     value=Qn,
                                     inv_coeff=False,
                                     ctrl='e')

            Nend = nodes[1]
            self += Transformer(label+'alpha'+str(n),
                                (N1, N2, N3, datum),
                                alpha=Rn)
            N1 = N2
    metadata = {'title': 'Flux-controlled fractional derivator',
                'component': 'Fracderfc',
                'label': 'fracder',
                'dico': 'fraccalc',
                'desc': r'Flux-controlled fractional derivator from [1]_ (chap 7):' + equation(r'e(s) = g \, s^{alpha}  \, f(s).'),
                'nodesdesc': "Component terminals with positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameters',
                'parameters': [['g', "Gain", 'unknown', 1.],
                               ['alpha', "Derivation order in (0, 1)", 'd.u.', 0.5],
                               ['NbPoles', "Approximation order", 'd.u.', 20],
                               ['PolesMinMax', "Poles modules in :math:`(10^{min}, 10^{max})`", 'Hz', (-5, 10)],
                               ['NbFreqPoints', "Number of optimization points", 'd.u.', 200],
                               ['FreqsMinMax', "Optimization interval", 'Hz', (1, 48e3)],
                               ['DoPlot', "Plot transfer function", 'bool', False]],
                'refs': {1: "Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016."},
                'nnodes': 36,
                'nedges': 68,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }
    # Write documentation
    __doc__ = componentDoc(metadata)

# ======================================================================= #



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
