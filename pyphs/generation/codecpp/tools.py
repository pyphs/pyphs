# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:01:13 2016

@author: Falaize
"""


def str_get_int(cpp, name):
    strget = "const unsigned int " + cpp.class_ref + "get_" + name \
        + "() const {\n    return " + name + ";\n}\n"
    return strget


def str_get_vec(cpp, name, dim):
    strget = ""
    strget += "\nvector<double> "
    strget += cpp.class_ref
    strget += "get_" + name + "() const { \n"
    strget += "    vector<double> v = vector<double>(get_" + dim + "());\n"
    strget += "    for (int i=0; i<get_" + dim + "(); i++) {\n"
    strget += "        v[i] = " + name + "[i];\n"
    strget += "    }\n"
    strget += "    return v;\n"
    strget += "    }"
    return strget
""


###############################################################################
###############################################################################
###############################################################################
###############################################################################

def build_args(simu):
    """
    define accessors and mutators of numerical values associated with arguments
    """

    names = {'vl', 'vnl', 'x', 'dx', 'dxnl', 'w', 'u', 'p'}

    for name in names:
        inds = getattr(simu.exprs, name + '_inds')
        setattr(simu, name, get_generator(inds))
        setattr(simu, 'set_' + name, set_generator(inds))

    # init args values with 0
    setattr(simu, 'args', numpy.array([0., ]*simu.exprs.nargs))


def build_funcs(simu):
    """
    link and lambdify all funcions for python simu
    """

    # generator of evaluation functions
    def eval_generator(name):
        expr = getattr(simu.exprs, name + '_expr')
        args = getattr(simu.exprs, name + '_args')
        inds = getattr(simu.exprs, name + '_inds')
        func = lambdify(args, expr,
                        subs=simu._phs.symbs.subs)

        if len(inds) > 0:
            inds = numpy.array(inds)
        else:
            inds = list()

        def eval_func():
            return func(*simu.args[inds])
        return eval_func

    # link evaluation to internal values
    names = {'dxH', 'y', 'z', 'update_lin',
             'impfunc', 'res_impfunc', 'jac_impfunc'}
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
    if simu._phs.is_nl():
        # update nl variables (dxnl and wnl)
        update_nl(simu)
    # update l variables (dxnl and wnl)
    update_l(simu)


def update_l(simu):
    vl = simu.update_lin()
    simu.set_vl(vl)


def update_nl(simu):
    # init it counter
    it = 0
    # init dx with 0
    simu.set_dxnl(numpy.array([0, ]*simu.exprs.nxnl))
    # init step on iteration
    step = float('Inf')
    # init residual of implicite function
    res = float('Inf')
    # init args memory for computation of step on iteration
    old_varsnl = numpy.array([float('Inf'), ]*simu.exprs.nnl)
    # loop while res > tol, step > tol and it < itmax
    while res > simu.config['numtol'] \
            and step > simu.config['numtol']\
            and it < simu.config['maxit']:
        # updated args
        iter_solver(simu)
        # eval residual
        res = simu.res_impfunc()
        # eval norm step
        step = simu.vnl() - old_varsnl
        step = numpy.sqrt(numpy.dot(step, step))
        # increment it
        it += 1
        # save args for comparison
        old_varsnl = simu.vnl().copy()


def iter_solver(simu):
    # eval args
    vnl = simu.vnl()
    impfunc = simu.impfunc().flatten()
    jac_impfunc = simu.jac_impfunc()
    # compute inverse jacobian
    ijac_impfunc = numpy.linalg.inv(jac_impfunc)
    # build updates for args
    vnl = vnl - numpy.dot(ijac_impfunc, impfunc)
    simu.set_vnl(vnl)

###############################################################################
###############################################################################
###############################################################################