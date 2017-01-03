# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 13:56:52 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

try:
    import itertools.izip as zip
except ImportError:
    pass

try:
    import itertools.imap as map
except ImportError:
    pass

def parallel_exec(funcs, args=None):
    """
    Parallel execution of each 'func' in 'funcs'.
    
    Warning
    -------
    Should not be used since for instance yields slower computations...

    Parameters
    ----------

    funcs : list
        List of functions.

    args : list, optional
        List of arguments (the default is None)

    Returns
    -------

    results : list
        List of results.

    Notes
    -----

    Chain Processes in Queue from multiprocessing.Manager().
    """
    # Check for functions
    assert isinstance(funcs, list), "'funcs' is not a list: {0!s}".format(type(funcs))
    nfuncs = len(funcs)

    # Check for arguments
    if args is None:
        args = [tuple(), ] * nfuncs
    else:
        assert isinstance(args, list), "'args' is not a list: {0!s}".format(type(args))

    def process_func(func, arg, pos, jobs):
        """
        Function called by Processes (put task in Queue).
        """
        jobs.put((pos, func(*arg)))


    from multiprocessing import Process

    # multiprocessing.Queue() can lead to deadlock so it is not used.
    # Queue from multiprocessing.Manager() is used instead
    if False:
        from multiprocessing import Manager
        manager = Manager()
        jobs = manager.Queue()
    else:
        from multiprocessing import Queue
        jobs = Queue()
    # Build and start workers
    i = 0
    workers = list()    
    for func, arg in zip(funcs, args):
        worker = Process(target=process_func, args=(func, arg, i, jobs))
        worker.daemon = True
        workers.append(worker)
        worker.start()
        i += 1
        
    # Get process results from the output queue
    results = [jobs.get() for _ in range(nfuncs)]

    # Exit the completed processes
    for worker in workers:
        worker.join()
        
    # Sort results
    results.sort()
    results = [r[1] for r in results]

    return results

def parallel_map(func, args):
    """
    Parallel execution of 'func' over arguments in 'args'.

    Parameters
    -----------

    func : function

    args : list of arguments

    Returns
    --------

    l : func(x) for x in args

    Notes
    ------
    Uses 'Pool' method from the 'multiprocessing' package with one process for each cpu core.

    """
    from multiprocessing import Pool, cpu_count
    pool = Pool(processes=cpu_count())
    result = pool.map(func, args)
    # For sake of safeness
    pool.close()
    pool.join()
    return result

def factorial(niter):
    """
    A simple function to test parallelization.
    """
    result = 1
    for i in range(1, niter+1):
        result *= i
    return result

def test_parallel_map(func=factorial, njobs=10000, arg=int(2*10**4)):
    """
    Compare performances of 'parallel_map' with serial list iterator.
    """
    args = [arg, ] * njobs
    import time
    # run parallel_map
    tinit = time.time()
    lpar = parallel_map(func, args)
    tpar = time.time() - tinit
    # run list iterator
    tinit = time.time()
    lser = [factorial(el) for el in args]
    tser = time.time() - tinit
    # test if same output
    test = all( el1 == el2 for (el1, el2) in zip(lser, lpar))
    print("time serial map: " + str(tser))
    print("time parallel map: " + str(tpar))
    print("Same output: " + str(test))
    print("improvement: " + str(tser/tpar))

def test_parallel_exec(func=factorial, njobs=10000, arg=int(2*10**4)):
    """
    Compare performances of 'parallel_exec' with serial list iterator.
    """
    args = [(arg, ), ] * njobs
    funcs = [func, ] * njobs
    import time
    # run parallel_map
    tinit = time.time()
    lpar = parallel_exec(funcs, args)
    tpar = time.time() - tinit
    # run list iterator
    tinit = time.time()
    lser = [factorial(*el) for el in args]
    tser = time.time() - tinit
    # test if same output
    test = all( el1 == el2 for (el1, el2) in zip(lser, lpar))
    print("time serial exec: " + str(tser))
    print("time parallel exec: " + str(tpar))
    print("Same output: " + str(test))
    print("improvement: " + str(tser/tpar))

if __name__ == '__main__':
    NJOBS = 100
    test_parallel_map(njobs=NJOBS)
    test_parallel_exec(njobs=NJOBS)
