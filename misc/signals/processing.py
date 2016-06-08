# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 18:57:15 2016

@author: Falaize
"""


def lowpass(s, fc, tbw=1e-2):
    """
    Lowpass filter of 1D object s.

    Parameters
    ----------

    s : Iterable or Generator
        Input signal
    fc : float
        Cutoff frequency as a fraction of the sampling rate (in (0, 0.5)).
    tbw : float, optional
        Transition band width, as a fraction of the cutoff frequency \
(in (0, 1), the default is 0.01).

    Return
    ------
    s_out : ndarray
        Low-pass version of input signal s.
    """

    from numpy import arange, cos, sinc, ceil, convolve, pi

    b = tbw*fc
    fc = fc-b
    N = int(ceil((4 / b)))
    if not N % 2:
        N += 1  # Make sure that N is odd.
    n = arange(N)
    # Compute sinc filter.
    h = sinc(2 * fc * (n - (N - 1) / 2.))
    # Compute Blackman window.
    w = 0.42 - 0.5 * cos(2 * pi * n / (N - 1)) + \
        0.08 * cos(4 * pi * n / (N - 1))
    # Multiply sinc filter with window.
    h = h * w
    # Normalize to get unity gain.
    h = h / sum(h)
    return convolve(s, h, 'same')
