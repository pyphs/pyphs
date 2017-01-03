# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 18:56:56 2016

@author: Falaize
"""
from processing import lowpass


def frequencyresponse(sigin, sigout, fs, nfft=None, filtering=None,
                      limits=None):
    """
    Return frequencies and modulus of \
transfer function T(iw) = sigout(iw)/sigin(iw).

    Parameters
    ----------

    sigin, sigout : array_like
        Time series of measurement values for input and output

    fs : float
        Sampling frequency

    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. \
If None, the FFT length is nperseg. Defaults to None.

    filtering : float, optional
        If provided, apply a lowpass filter on sigin and sigout before \
computing fft (the default is None). Then filtering is the cutoff frequency \
as a fraction of the sampling rate (in (0, 0.5)).

    limits : (fmin, fmax), optional
        If provided, truncates the output between fmin and fmax \
(the default is None).

    Return
    ------

    f : list
        frequency point in Hertz.

    TF : list
        Modulus of transfer function.

    """
    if filtering is not None:
        sigin = lowpass(sigin, fc=filtering)
        sigout = lowpass(sigout, fc=filtering)
    import scipy.signal as sig
    f, Pxx_den1 = sig.welch(sigin, fs, nperseg=nfft, scaling='spectrum')
    f, Pxx_den2 = sig.welch(sigout, fs, nperseg=nfft, scaling='spectrum')
    TF = Pxx_den2/Pxx_den1
    if limits is None:
        fmin, fmax = 20., 20e3
    else:
        fmin, fmax = limits
    from numpy import nonzero
    nfmax = len(f) if fmax >= f[-1] else nonzero(f > fmax)[0][0]
    nfmin = nonzero(f > fmin)[0][0]
    f = f[nfmin:nfmax]
    TF = [el**0.5 for el in TF[nfmin:nfmax]]
    return f, TF
