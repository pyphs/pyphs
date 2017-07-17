# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:27:55 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from pyphs.core.tools import types as core_types
from ..tools import types as num_types
from ..tools import lambdify, Operation
from pyphs.config import VERBOSE, CONFIG_NUMERIC
import numpy


# =========================================================================== #

class Numeric(object):
    """
    This class implements a numerical version of Core. First, a numerical
    method is applied symbolically to a core, then every relevant functions
    for simulations are lambdified and organized into the object.
    """
    def __init__(self, method, inits=None, label=None, config=None):
        """
        Instanciate a Numeric.
    
        Parameters
        ----------
    
        method : pyphs.Method
            Symbolic numerical method to lambdify.
        
        inits : dict or None (optional)
            Dictionary with variable name as keys and initialization values
            as value. E.g: inits = {'x': [0, 0, 1]} to initalize state x
            with dim(x) = 3, x[0] = x[1] = 0 and x[2] = 1.
            
        Return
        ------
        numeric : pyphs.Numeric
        """
        # Save method object
        self.method = method
        
        if label is None:
            label = self.method.label
        self.label = label

        # Manage configuration
        self.config = CONFIG_NUMERIC.copy()
        if config is None:
            config = {}
        for k in config.keys():
            if k not in self.config.keys():
                raise AttributeError('Unknown parameter {}.'.format(k))
        self.config.update(config)
        self.method.subs.update({self.method.fs: self.config['fs']})

        # Define inits
        self.inits = {}        
        if inits is not None:
            self.inits.update(inits)
            
        self.build()
            
    def init(self):
        """
        Set initilization values of self.
        
        """
        for k in self.inits.keys():
            val = self.inits[k]
            get_func = getattr(self, k)
            self_shape = get_func().shape
            set_func = getattr(self, 'set_' + k)                
            if val is None:
                val = numpy.zeros(self_shape)                
                set_func(val)
            else:                
                val = numpy.asarray(val)
                if not val.shape == self_shape:
                    text = 'Init value for {0} has wrong shape {1}'.format(k, val.shape)
                    raise TypeError(text)
                else:
                    set_func(val)
                
    def build(self):

        if VERBOSE >= 1:
            print('Build numeric {}...'.format(self.label))

        # init args values with 0
        self.args = numpy.array([0., ]*self.method.dims.args())

        # build evaluations for arguments
        for name in self.method.args_names:
            self._build_arg(name)
            
        # init values for arguents
        self.init()
        

        # build numerical evaluation for functions and operations
        for name in self.method.update_actions_deps():
            self._build_eval(name)

    def _build_arg(self, name):
        """
        Define accessors and mutators for numerical values associated with
        numerical arguments.
        """
        inds = getattr(self.method, name + '_inds')
        setattr(self, name, getarg_generator(self, name, inds))
        setattr(self, 'set_' + name, setarg_generator(self, name, inds))

    def _build_func(self, name):
        """
        Link and lambdify a numerical function for python from its name.
        """
        # link evaluation to internal values
        func = evalfunc_generator(self, name)
        value = func()
        setattr(self, name + '_eval', func)
        setattr(self, '_' + name, value)
        setattr(self, name, getfunc_generator(self, name))
        setattr(self, 'set_' + name, setfunc_generator(self, name))

    def _build_op(self, name):
        """
        Link and lambdify a numerical operation from its name.
        """
        # build a callable func() that evaluate the operation
        func = evalop_generator(self, name,
                                getattr(self.method, name + '_op'))
        # store the function
        setattr(self, name + '_eval', func)

        # evaluate to initialize
        value = func()
        # store the value
        setattr(self, '_' + name, value)

        # accessor
        setattr(self, name, getfunc_generator(self, name))
        # mutator
        setattr(self, 'set_' + name, setfunc_generator(self, name))

    def _build_eval(self, name):
        """
        Link and lambdify a numerical operation or numerical function from name
        """
        if VERBOSE >= 2:
            print('    Build numerical evaluation of {}'.format(name))
        # build for sympy.expression
        if name in self.method.funcs_names:
            self._build_func(name)
        # build for Operation
        elif name in self.method.ops_names:
            #  build of dependencies before hand
            deps = getattr(self.method, name + '_deps')
            for dep in deps:
                if not hasattr(self, dep):
                    self._build_eval(dep)
            self._build_op(name)

    def update(self, u=None, p=None):
        """
        update
        ******

        Update every quantities according to the update method defined in the
        argument :code:`update_actions`.

        Parameters
        ----------

        u : numpy array
            Input vector.

        p : numpy array
            Parameters vector.
        """

        if u is None:
            u = numpy.zeros(self.method.dims.y())

        if p is None:
            p = numpy.zeros(self.method.dims.p())

        self.set_u(u)
        self.set_p(p)
        for action in self.method.update_actions:
            actiontype = action[0]
            if actiontype == 'exec':
                self._execs(action[1])
            else:
                self._iterexecs(*action[1])

    def _execs(self, commands):
        """
        Execute a command
        """
        for command in commands:
            if isinstance(command, str):
                setname = command
                evalname = setname
            else:
                setname = command[0]
                evalname = command[1]
            setfunc = getattr(self, 'set_'+setname)
            evalfunc = getattr(self, evalname + '_eval')
            setfunc(evalfunc())

    def _iterexecs(self, commands, res_name, step_name):
        """
        Execute iteratively a command until res_name<eps or step_name<eps or
        number of iterations>itmax, where eps and itmax are defined in the
        dictionary method.config.
        """
        # init it counter
        self.it = 0
        # init step on iteration
        getattr(self, 'set_' + step_name)(1.)
        # loop while res > tol, step > tol and it < itmax
        while getattr(self, res_name)() > self.config['eps'] \
                and getattr(self, step_name)() > self.config['eps']\
                and self.it < self.config['maxit']:
            self._execs(commands)
            self.it += 1
        if self.it >= self.config['maxit'] and VERBOSE >= 1:
            message = 'Warning: {} = {} after {} iterations'
            print(message.format(res_name,
                                 getattr(self, res_name)(),
                                 self.it))


# =========================================================================== #

def evalfunc_generator(nums, name):
    """
    Return an evaluator of the function :code:`getarg(nums.method, names + '_expr')`,
    with a mapping to some of the arguments in :code:`nums.args`, using
    sympy or theano lambdification.

    Parameters
    ----------

    nums : Numeric

    name : str

    Return
    ------

    func : function
        Evaluator
    """
    expr = getattr(nums.method, name + '_expr')
    args = getattr(nums.method, name + '_args')
    inds = getattr(nums.method, name + '_inds')
    func = lambdify(args, expr, subs=nums.method.subs,
                    theano=nums.config['theano'])

    if len(inds) > 0:
        inds = numpy.array(inds)
    else:
        inds = list()

    def eval_func():
        return func(*nums.args[inds])

    if isinstance(expr, core_types.scalar_types):
        num_types.scalar_test(eval_func())
    elif isinstance(expr, core_types.vector_types):
        num_types.vector_test(eval_func())
    elif isinstance(expr, core_types.matrix_types):
        num_types.matrix_test(eval_func())
    else:
        raise TypeError('Lambdified function output type not understood.')

    eval_func.func_doc = """
        Evaluate :code:`{0}`.

        Return
        ------

        _{0} : numpy array
            The current evaluation of :code:`{0}`, with shape {1}.
    """.format(name, eval_func().shape)

    return eval_func


def evalop_generator(nums, name, op):
    """
    Return an evaluator of the function :code:`getarg(nums, names + '_expr')`.
    """
    args = list()
    for arg in op.args:
        if isinstance(arg, Operation):
            args.append(evalop_generator(nums, name, arg))
        elif isinstance(arg, str):
            args.append(getattr(nums, arg))
        elif arg is None:
            args.append(numpy.array([]))
        else:
            assert isinstance(arg, (int, float))
            args.append(arg)
    func = Operation(op.operation, args)

    def eval_func():
        return func()

    eval_func.func_doc = """
        Evaluate :code:`{0}`.

        Return
        ------

        _{0} : numpy array
            The current evaluation of :code:`{0}`, with shape {1}.
    """.format(name, func().shape)

    return eval_func


# =========================================================================== #

def getarg_generator(nums, name, inds):
    """
    generators of 'get'
    """
    if len(inds) > 0:
        inds = numpy.array(inds)
    else:
        inds = list()

    def get_func():
        return nums.args[inds]

    get_func.func_doc = """
        Accessor to the value of :code:`{0}`.

        Return
        ------

        _{0} : numpy array
            The current value of :code:`{0}`, with shape ({2}, ). It
            corresponds to :code:`{0}={1}`.
        """.format(name, [nums.method.args()[i] for i in inds], len(inds))

    return get_func


def setarg_generator(nums, name, inds):
    """
    generators of 'set'
    """
    if len(inds) > 0:
        inds = numpy.array(inds)
    else:
        inds = list()

    def set_func(array):
        nums.args[inds] = array

    set_func.func_doc = """
        Change the value of :code:`{0}`.

        Parameter
        ------

        array : numpy array
            The new value of :code:`{0}`, with shape ({2}). It corresponds to
            :code:`{0}={1}`

        """.format(name, [nums.method.args()[i] for i in inds], len(inds))

    return set_func


# =========================================================================== #

def getfunc_generator(nums, name):
    """
    generators of 'get'
    """
    def get_func():
        return getattr(nums, '_' + name)
    get_func.func_doc = """
        Accessor to the value of {0}.

        Return
        ------

        _{0} : numpy array
            The current value of :code:`{0}`, with shape {1}.
        """.format(name, getattr(nums, '_'+name).shape)
    return get_func


def setfunc_generator(nums, name):
    """
    generators of 'set'
    """

    def set_func(array):
        setattr(nums, '_' + name, array)
    set_func.func_doc = """
        Change the value of {0}.

        Parameter
        ---------

        array : numpy array
            The new value of :code:`{0}`, with shape {1}.
        """.format(name, getattr(nums, '_'+name).shape)
    return set_func
