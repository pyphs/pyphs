# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 15:50:14 2016

@author: Falaize
"""

import signal


_dur_process_max = 1.


# Register an handler for the timeout
def handler(signum, frame):
    print "A process has been ignored."
    raise Exception("time out")


def timeout(func, arg, dur=_dur_process_max):
    # Register the signal function handler
    signal.signal(signal.SIGALRM, handler)

    # Define a timeout for your function
    signal.alarm(dur)

    try:
        arg = func(arg)
        # Cancel the timer if the function returned before timeout
        signal.alarm(0)
        success = True
    except Exception, exc:
        success = False
        print exc
        pass
    return arg, success
