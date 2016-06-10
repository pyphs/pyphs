# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:31:24 2016

@author: Falaize
"""

from pypHs import pHobj
import sympy as sp
import numpy as np
from sympy.physics import units

class FracDerEffortCtrl(pHobj):
    """ Fractional Effort Controlled springpot element
    usgae: FracDerEffortCtrl label ['n1','n2'] [rAlphaMag, alphaMag ,NbPoles]

    """
    def __init__(self, label, nodes_labels, value):
        pHobj.__init__(self,label)
        if  list(value).__len__()==3:
            OptimFreqsMinMax=(20,20e3)
        elif list(value).__len__()==4:
            OptimFreqsMinMax=value[3]
        print('\n')
        print(str(OptimFreqsMinMax))
        diagRmu, diagQmu = fractionalDifferenciatorWeights(value[0], value[1], NbPoles=value[2], OptimFreqsMinMax=OptimFreqsMinMax)
        nbPoles = diagRmu.__len__()
        subs = {}
        for n in range(nbPoles):
            self.AddLinearDissipativeComponents(['w'+label+str(n)],[diagRmu[n]], [1])
            edge_data_dic = {'ref':'w'+label+str(n), 'type':'dissipative', 'realizability':'effort_controlled', 'linear':True, 'link_ref':'w'+label+str(n)}
            self.Graph.add_edges_from([(nodes_labels[0], 'N'+label+str(n)+"_1", edge_data_dic)])

            self.AddLinearStorageComponents(["x"+label+str(n)],[diagQmu[n]], [1])
            edge_data_dic = {'ref':"x"+label+str(n), 'type':'storage', 'realizability':'flux_controlled', 'linear':True, 'link_ref':"x"+label+str(n)}
            self.Graph.add_edges_from([('N'+label+str(n)+"_2", 0, edge_data_dic)])

            Symb = sp.symbols('alpha'+label+str(n))
            self.AddTransformers(label+str(n), "transformer", Symb)        
            labels = ['y_'+label+str(n)+'_'+str(e) for e in (1,2)]
            edge_data_dic1 = {'type':'trans_port', 'realizability':'?', 'ref':labels[0], 'link_ref':labels[1], 'linear':'?'}
            edge_data_dic2 = {'type':'trans_port', 'realizability':'?', 'ref':labels[1], 'link_ref':labels[0], 'linear':'?'}
            edges = [('N'+label+str(n)+"_1", nodes_labels[1], edge_data_dic1),('N'+label+str(n)+"_2", 0, edge_data_dic2)]
            self.Graph.add_edges_from(edges)

            subs.update({str(Symb):diagRmu[n]**-1})

        self.subs.update(subs)

class FracDerFluxCtrl(pHobj):
    """ Fractional Flux Controlled storage element
    usgae: FracIntEffortCtrl label ['n1','n2'] [rAlphaMag, alphaMag ,NbPoles, (fmin, fmax)]

    """
    def __init__(self, label, nodes_labels, value):
        pHobj.__init__(self,label)
        if list(value).__len__()==3:
            OptimFreqsMinMax=(20,20e3)
        elif list(value).__len__()==4:
            OptimFreqsMinMax=value[3]
        print('\n')
        print(str(OptimFreqsMinMax))
        diagRmu, diagQmu = fractionalDifferenciatorWeights(value[0], value[1], NbPoles=value[2], OptimFreqsMinMax=OptimFreqsMinMax)
        nbPoles = diagRmu.__len__()
        subs = {}
        nodes = [nodes_labels[0],]+['N'+label+str(n) for n in range(1,nbPoles)] + [nodes_labels[1],]
        nodes.reverse()
        for n in range(nbPoles):
            N1 = nodes.pop()
            N2 = nodes[-1]

            self.AddLinearDissipativeComponents(['w'+label+str(n)],[diagRmu[n]], [1])
            edge_data_dic = {'ref':'w'+label+str(n), 'type':'dissipative', 'realizability':'flux_controlled', 'linear':True, 'link_ref':'w'+label+str(n)}
            self.Graph.add_edges_from([(N1, N2, edge_data_dic)])

            self.AddLinearStorageComponents(["x"+label+str(n)],[diagQmu[n]], [1])
            edge_data_dic = {'ref':"x"+label+str(n), 'type':'storage', 'realizability':'effort_controlled', 'linear':True, 'link_ref':"x"+label+str(n)}
            self.Graph.add_edges_from([(str(N1)+"trans"+str(n), 0, edge_data_dic)])

            Symb = sp.symbols('alpha'+label+str(n))
            self.AddTransformers(label+str(n), "transformer", Symb)        
            labels = ['y_'+label+str(n)+'_'+str(e) for e in (1,2)]
            edge_data_dic1 = {'type':'trans_port', 'realizability':'?', 'ref':labels[0], 'link_ref':labels[1], 'linear':'?'}
            edge_data_dic2 = {'type':'trans_port', 'realizability':'?', 'ref':labels[1], 'link_ref':labels[0], 'linear':'?'}
            edges = [(N1, N2, edge_data_dic1),(str(N1)+"trans"+str(n), 0, edge_data_dic2)]
            self.Graph.add_edges_from(edges)

            subs.update({str(Symb):diagRmu[n]**-1})

        self.subs.update(subs)

class FracIntEffortCtrl(pHobj):
    """ Fractional Flux Controlled storage element
    usgae: FracIntEffortCtrl label ['n1','n2'] [rAlphaMag, beta ,NbPoles]

    """
    def __init__(self, label, nodes_labels, value):
        pHobj.__init__(self,label)
        if list(value).__len__()==3:
            OptimFreqsMinMax=(20,20e3)
        elif list(value).__len__()==4:
            OptimFreqsMinMax=value[3]
        print(OptimFreqsMinMax)
        diagRmu, diagQmu = fractionalDifferenciatorWeights(value[0], value[1], NbPoles=value[2], OptimFreqsMinMax=OptimFreqsMinMax)
        nbPoles = diagRmu.__len__()
        for n in range(nbPoles):
            self.AddLinearDissipativeComponents(['w'+label+str(n)],[diagRmu[n]], [1])
            edge_data_dic = {'ref':'w'+label+str(n), 'type':'dissipative', 'realizability':'flux_controlled', 'linear':True, 'link_ref':'w'+label+str(n)}
            self.Graph.add_edges_from([('node'+label+str(n),nodes_labels[1], edge_data_dic)])

            self.AddLinearStorageComponents(["x"+label+str(n)],[diagQmu[n]], [1])
            edge_data_dic = {'ref':"x"+label+str(n), 'type':'storage', 'realizability':'effort_controlled', 'linear':True, 'link_ref':"x"+label+str(n)}
            self.Graph.add_edges_from([(nodes_labels[0],'node'+label+str(n), edge_data_dic)])

class FracIntFluxCtrl(pHobj):
    """ Fractional Flux Controlled storage element
    usgae: FracIntFluxCtrl label ['n1','n2'] [rAlphaMag, alphaMag ,NbPoles]

    """
    def __init__(self, label, nodes_labels, value):
        pHobj.__init__(self,label)
        diagRmu, diagQmu = fractionalIntegratorWeights(value[0], value[1], NbPoles=value[2])
        nbPoles = diagRmu.__len__()
        nodes = [nodes_labels[0],]+['node'+label+str(n) for n in range(1,nbPoles)] + [nodes_labels[1],]
        nodes.reverse()
        for n in range(nbPoles):
            N1 = nodes.pop()
            N2 = nodes[-1]

            self.AddLinearDissipativeComponents(['w'+label+str(n)],[diagRmu[n]], [1])
            edge_data_dic = {'ref':'w'+label+str(n), 'type':'dissipative', 'realizability':'effort_controlled', 'linear':True, 'link_ref':'w'+label+str(n)}
            self.Graph.add_edges_from([(N1, N2, edge_data_dic)])

            self.AddLinearStorageComponents(["x"+label+str(n)],[diagQmu[n]], [1])
            edge_data_dic = {'ref':"x"+label+str(n), 'type':'storage', 'realizability':'flux_controlled', 'linear':True, 'link_ref':"x"+label+str(n)}
            self.Graph.add_edges_from([(N1,N2, edge_data_dic)])

def fractionalIntegratorWeights(p, beta, NbPoles=20, OptimPolesMinMax=(-10,10),  NbFreqPoints=200, OptimFreqsMinMax=(1, 48e3), DoPlot=True):
    
    # Defintion of the frequency grid
    fmin, fmax = OptimFreqsMinMax
    wmin, wmax = 2*np.pi*fmin, 2*np.pi*fmax 
    w = np.exp( np.log(wmin) + np.linspace(0,1,NbFreqPoints+1)*np.log(wmax/wmin) )
    w12 = np.sqrt(w[1:]*w[:-1])

    # Unpack min and max exponents to define the list of poles
    emin, emax = OptimPolesMinMax
    Xi  = np.logspace(emin, emax, NbPoles) # xi_0 -> xi_{N+1}
    
    # Input to Output transfer function of the fractional integrator
    transferFunctionFracInt = lambda s: s**-beta
    
    # Target transfer function evaluated on the frequency grid
    T = transferFunctionFracInt(1j*w12)
    
    # Return the basis vector of elementary damping with poles Xi
    Basis = lambda s, Xi: (s+Xi)**-1

    # Matrix of basis transfer function for each poles on the frequency grid
    M = np.zeros((NbFreqPoints,NbPoles), dtype = np.complex64)    
    for k in np.arange(NbFreqPoints):
        M[k,:] = Basis(1j*w12[k], Xi)    

    # Perceptual weights
    WBuildingVector = (np.log(w[1:])-np.log(w[:-1]))/(np.abs(T)**2)
    W = np.diagflat(WBuildingVector)
    
    # Definition of the cost function
    CostFunction = lambda mu: (np.dot(np.conjugate((np.dot(M,mu) - T).T),np.dot(W,np.dot(M,mu) - T))).real
    
    # Optimization constraints
    bnds = [(0,None) for n in range(NbPoles)]
   
    # Optimization
    from scipy.optimize import minimize
    MuOpt = minimize(CostFunction, np.ones(NbPoles), bounds=bnds, tol=eps)
    Mu = MuOpt.x # Get the solution

    # Conversion to phs parameters
    diagQ = []
    diagR = []

    # Eliminate 0 valued weigths    
    for n in np.arange(NbPoles):
        if Mu[n]>0:
            pn = p*Mu[n]**-1
            diagR.append(pn*Xi[n])
            diagQ.append(pn**-1)

    if DoPlot:
        from matplotlib.pyplot import figure, subplot, plot, loglog, semilogx, ylabel, legend, grid, xlabel     
        TOpt = np.array(M*np.matrix(Mu).T)
        wmin, wmax = 2*np.pi*fmin, 2*np.pi*fmax
        figure()
        subplot(2,1,1)
        faxis = w12[(wmin<w12)&(w12<wmax)]/(2*np.pi)
        v1 = 20*np.log10(np.abs(T[(wmin<w12)&(w12<wmax)]))
        v2 = 20*np.log10(np.abs(TOpt[(wmin<w12)&(w12<wmax)]))
        v3 = map(lambda x,y: x-y, v1, v2)
        semilogx(faxis,v1,label = 'Target') 
        semilogx(faxis,v2, label = 'Approx')
        ylabel('Transfert (dB)')
        legend(loc = 0)
        grid()        
        subplot(2,1,2)
        plot(faxis, v3, label = 'Error')
        xlabel('Log-frequencies (log Hz)')
        ylabel('Error (dB)')
        legend(loc = 0)
        grid()        
    
    return diagR, diagQ

def fractionalDifferenciatorWeights(p, alpha, NbPoles=20, OptimPolesMinMax=(-5,10),  NbFreqPoints=200, OptimFreqsMinMax=(1, 48e3), DoPlot=True):
    print(OptimFreqsMinMax)

    # Defintion of the frequency grid
    fmin, fmax = OptimFreqsMinMax
    wmin, wmax = 2*np.pi*fmin, 2*np.pi*fmax 
    w = np.exp( np.log(wmin) + np.linspace(0,1,NbFreqPoints+1)*np.log(wmax/wmin) )
    w12 = np.sqrt(w[1:]*w[:-1])

    # Unpack min and max exponents to define the list of poles
    emin, emax = OptimPolesMinMax
    Xi  = np.logspace(emin, emax, NbPoles) # xi_0 -> xi_{N+1}
    
    # Input to Output transfer function of the fractional integrator of order 1-alpha
    beta = 1.-alpha
    transferFunctionFracInt = lambda s: s**-beta
    
    # Target transfer function evaluated on the frequency grid
    T = transferFunctionFracInt(1j*w12)
    
    # Return the basis vector of elementary damping with poles Xi
    Basis = lambda s, Xi: (s+Xi)**-1

    # Matrix of basis transfer function for each poles on the frequency grid
    M = np.zeros((NbFreqPoints,NbPoles), dtype = np.complex64)    
    for k in np.arange(NbFreqPoints):
        M[k,:] = Basis(1j*w12[k], Xi)    

    # Perceptual weights
    WBuildingVector = (np.log(w[1:])-np.log(w[:-1]))/(np.abs(T)**2)
    W = np.diagflat(WBuildingVector)
    
    # Definition of the cost function
    CostFunction = lambda mu: (np.dot(np.conjugate((np.dot(M,mu) - T).T),np.dot(W,np.dot(M,mu) - T))).real
    
    # Optimization constraints
    bnds = [(0,None) for n in range(NbPoles)]
   
    # Optimization
    from scipy.optimize import minimize
    MuOpt = minimize(CostFunction, np.ones(NbPoles), bounds=bnds, tol=eps)
    Mu = MuOpt.x # Get the solution

    # Conversion to phs parameters
    diagQ = []
    diagR = []

    # Eliminate 0 valued weigths    
    for n in np.arange(NbPoles):
        if Mu[n]>0:
            diagR.append(p*Mu[n])
            diagQ.append(p*Mu[n]*Xi[n])

    if DoPlot:
        from matplotlib.pyplot import figure, subplot, plot, loglog, semilogx, ylabel, legend, grid, xlabel     
        TOpt = np.array(M*np.matrix(Mu).T)
        wmin, wmax = 2*np.pi*fmin, 2*np.pi*fmax
        figure()
        subplot(2,1,1)
        faxis = w12[(wmin<w12)&(w12<wmax)]/(2*np.pi)
        v1 = 20*np.log10(np.abs(T[(wmin<w12)&(w12<wmax)]))
        v2 = 20*np.log10(np.abs(TOpt[(wmin<w12)&(w12<wmax)]))
        v3 = map(lambda x,y: x-y, v1, v2)
        semilogx(faxis,v1,label = 'Target') 
        semilogx(faxis,v2, label = 'Approx')
        ylabel('Transfert (dB)')
        legend(loc = 0)
        grid()        
        subplot(2,1,2)
        plot(faxis, v3, label = 'Error')
        xlabel('Log-frequencies (log Hz)')
        ylabel('Error (dB)')
        legend(loc = 0)
        grid()        
    
    return diagR, diagQ
