# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 15:50:14 2016

@author: Falaize
"""

import signal


_dur_process_max = 5


# Register an handler for the timeout
def handler(signum, frame):
    print "A process has been ignored."
    raise Exception("time out")


def timeout(func, arg):
    # Register the signal function handler
    signal.signal(signal.SIGALRM, handler)

    # Define a timeout for your function
    signal.alarm(_dur_process_max)

    try:
        arg = func(arg)
        # Cancel the timer if the function returned before timeout
        signal.alarm(0)
    except Exception, exc:
        print exc
        pass
    return arg
