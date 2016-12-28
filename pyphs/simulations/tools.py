# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 20:42:08 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function
from pyphs.numerics.tools import lambdify
import numpy


def build_args(simu):
    """
    define accessors and mutators of numerical values associated with arguments
    """
    # generators of 'get' and 'set':
    def get_generator(inds):
        if len(inds) > 0:
            inds = numpy.array(inds)
        else:
            inds = list()

        def get_func():
            return simu.args[inds]

        return get_func

    def set_generator(inds):
        if len(inds) > 0:
            inds = numpy.array(inds)
        else:
            inds = list()

        def set_func(array):
            simu.args[inds] = array.flatten()

        return set_func

    names = {'vl', 'vnl',
             'x', 'dx',
             'xl', 'dxl',
             'xnl', 'dxnl',
             'w', 'wl', 'wnl',
             'u', 'p'}

    for name in names:
        inds = getattr(simu.Exprs, name + '_inds')
        setattr(simu, name, get_generator(inds))
        setattr(simu, 'set_' + name, set_generator(inds))

    # init args values with 0
    setattr(simu, 'args', numpy.array([0., ]*simu.Exprs.nargs))


def build_funcs(simu):
    """
    link and lambdify all functions for python simulation
    """

    # generator of evaluation functions
    def eval_generator(name):
        expr = getattr(simu.Exprs, name + '_expr')
        args = getattr(simu.Exprs, name + '_args')
        inds = getattr(simu.Exprs, name + '_inds')
        func = lambdify(args, expr,
                        subs=simu.Core.subs)

        if len(inds) > 0:
            inds = numpy.array(inds)
        else:
            inds = list()

        def eval_func():
            return func(*numpy.array(simu.args[inds]))
        return eval_func

    # link evaluation to internal values
    names = {'dxH', 'y', 'z'}
    if simu.config['presolve']:
        names = names.union({'update_lin', 'impfunc',
                             'res_impfunc', 'jac_impfunc'})
    else:
        names = names.union({'iDl', 'barNlxl', 'barNlnl', 'barNly',
                             'barNnlxl', 'barNnll', 'barNnlnl', 'Inl',
                             'fnl', 'jac_fnl', 'barNnly'})
    for name in names:
        setattr(simu, name, eval_generator(name))


def update(simu, u, p):
    """
    update with input 'u' and parameter 'p' on the time step (samplerate \
is numerics.fs).
    """
    # store u in numerics
    simu.set_u(u)
    # store p in numerics
    simu.set_p(p)
    # update state from previous iteration
    simu.set_x(simu.x() + simu.dx())
    if not simu.config['presolve']:
        # Update system matrices if presolve did not succeed
        if bool(simu.Core.dims.xl()):
            setattr(simu, 'Dl', numpy.linalg.inv(simu.iDl()))
        else:
            setattr(simu, 'Dl', simu.iDl())
        setattr(simu, 'Nlxl', numpy.dot(simu.Dl, simu.barNlxl()))
        setattr(simu, 'Nlnl', numpy.dot(simu.Dl, simu.barNlnl()))
        setattr(simu, 'Nly', numpy.dot(simu.Dl, simu.barNly()))
    if simu.Core.is_nl():
        # update nl variables (dxnl and wnl)
        update_nl(simu)
    # update l variables (dxnl and wnl)
    update_l(simu)


def update_l(simu):
    if simu.config['presolve']:
        vl = simu.update_lin()
        simu.set_vl(vl)
    else:
        vl = numpy.dot(simu.Nlxl, simu.xl()) + \
            numpy.dot(simu.Nlnl, simu.fnl()) + numpy.dot(simu.Nly, simu.u())
        simu.set_vl(vl)

def update_nl(simu):
    # init it counter
    it = 0
    # init dx with 0
    simu.set_dxnl(numpy.array([0, ]*simu.Exprs.nxnl))
    # init step on iteration
    step = float('Inf')
    # init residual of implicite function
    res = float('Inf')
    # init args memory for computation of step on iteration
    old_varsnl = numpy.array([float('Inf'), ]*simu.Exprs.nnl)

    # loop while res > tol, step > tol and it < itmax
    while res > simu.config['numtol'] \
            and step > simu.config['numtol']\
            and it < simu.config['maxit']:
        if not simu.config['presolve']:
            # Update system matrices if presolve did not succeed
            if simu.Core.dims.xl() == 0:
                temp = numpy.zeros((simu.Core.dims.xnl()+simu.Core.dims.wnl(),
                                    simu.Core.dims.xl()))
            else:
                temp = simu.barNnlxl() + numpy.dot(simu.barNnll(),
                                                   simu.barNlxl())
            setattr(simu, 'Nnlxl', temp)

            setattr(simu, 'Nnlnl',
                    simu.barNnlnl() + numpy.dot(simu.barNnll(),
                                                simu.barNlnl()))

            if simu.Core.dims.y() == 0:
                temp = numpy.zeros((simu.Core.dims.xnl()+simu.Core.dims.wnl(),
                                    simu.Core.dims.y()))
            elif simu.Core.dims.xl() == 0:
                temp = simu.barNnly()
            else:
                temp = simu.barNnly() + numpy.dot(simu.barNnll(),
                                                  simu.barNly())

            setattr(simu, 'Nnly', temp)

            setattr(simu, 'c',
                    numpy.dot(simu.Nnlxl, simu.xl()) +
                    numpy.dot(simu.Nnly, simu.u()))
            simu.impfunc = (numpy.dot(simu.Inl(), simu.vnl()) -
                            numpy.dot(simu.Nnlnl, simu.fnl().flatten()) -
                            simu.c)
            # updated args
            iter_solver(simu)
            # eval residual
            res = float(numpy.sqrt(numpy.dot(simu.impfunc, simu.impfunc)))
        else:
            # updated args
            iter_solver_presolve(simu)
            # eval residual
            res = simu.res_impfunc()

        # eval norm step
        step = simu.vnl() - old_varsnl
        step = numpy.sqrt(numpy.dot(step, step))
        # increment it
        it += 1
        # save args for comparison
        old_varsnl = simu.vnl().copy()


def iter_solver_presolve(simu):
    # eval args
    vnl = simu.vnl()
    impfunc = simu.impfunc().flatten()
    jac_impfunc = simu.jac_impfunc()
    # compute inverse jacobian
    ijac_impfunc = numpy.linalg.inv(jac_impfunc)
    # build updates for args
    vnl = vnl - numpy.dot(ijac_impfunc, impfunc)
    simu.set_vnl(vnl)


def iter_solver(simu):
    # eval args
    vnl = simu.vnl()
    impfunc = simu.impfunc.flatten()
    jac_impfunc = simu.Inl() - numpy.dot(simu.Nnlnl, simu.jac_fnl())
    # compute inverse jacobian
    ijac_impfunc = numpy.linalg.inv(jac_impfunc)
    # build updates for args
    vnl = vnl - numpy.dot(ijac_impfunc, impfunc)
    simu.set_vnl(vnl)
    simu.impfunc = (numpy.dot(simu.Inl(), vnl) -
                    numpy.dot(simu.Nnlnl, simu.fnl().flatten()) -
                    simu.c)
