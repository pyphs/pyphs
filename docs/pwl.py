#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 00:41:28 2016

@author: Falaize
"""

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

sx = sp.symbols('x')
f = sx**3

fn = sp.lambdify(sx, f)
dfn = sp.lambdify(sx, f.diff(sx))

xmin = -5
xmax = 5
nx = 10
nxinf = int(nx/2)
nxsup = nx-nxinf-1

nopt = int(1e3)


xinf = np.linspace(xmin, xmin/nxinf, nxinf) 
x0 = np.zeros(1)
xsup = np.linspace(xmax/nxsup, xmax, nxsup)
x = np.concatenate((xinf, x0, xsup)) 

xref = np.linspace(xmin, xmax, nopt) 
fref = [fn(ex) for ex in xref]

allsx = sp.symbols(['x'+str(n) for n in range(nx)])
        
# parts = [(f.subs({sx: allsx[0]}) + (sx-allsx[0])*(f.subs({sx: allsx[1]})-f.subs({sx: allsx[0]})), sx <= xmin)]
# for n in range(1, nx):
  #   parts += [(f.subs({sx: allsx[n-1]}) + ((sx-allsx[n-1])/((allsx[n]-allsx[n-1])))*(f.subs({sx: allsx[n]})-f.subs({sx: allsx[n-1]})), sx <= allsx[n])]
    
        
# pwf = sp.Piecewise(*parts)

# lse = sum([(elf-pwf.subs({sx: elx}))**2 for (elf, elx) in zip(fref, xref.tolist())]).simplify()

# lsen = sp.lambdify(allsx, lse, dummify=False)

# from scipy.optimize import minimize

# res = minimize(lambda xx: lsen(*xx) , x)
       
plt.plot(fref, '-o')