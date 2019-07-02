# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 18:56:56 2016

@author: Falaize
"""
from .processing import lowpass
from pyphs.misc.plots.tools import (annotate, standard)
from pyphs.misc.plots.fonts import globalfonts
import numpy as np


def spectrogram(x, fs, show=False, **kwargs):
    """
    Plot spectrogramm of datay.

    Parameters
    ----------

    x : lists of values
        y-axis values for each curve.

    fs : floats
        samplerate.

    label : list, optional
        signal label (the default is None).

    xlabel : str, optional
        x-axis label (the default is None).

    ylabel : list of str, optional
        y-axis labels (the default is None).

    path : str, optional
        Figure is saved in 'filelabel.png' (the default is 'multiplot').

    title : str, optional
        Figure main title. If set to None, the desactivated (the default is
        None).

    dynamics : positive value, optional
        The dynamics is normalized to 0db and the value below minus 'dynamics'
        are set to zeros

    cmap : str, optional
        Colormap specifier. Default is 'gnuplot2'.
    """
    opts = standard.copy()
    opts['ylabel'] = opts.pop('ylabels')
    opts['label'] = opts.pop('labels')
    opts.update(kwargs)

    if not 'dynamics' in opts.keys():
        opts['dynamics'] = 80.
    if not 'nfft' in opts.keys():
        opts['nfft'] = int(2**8)
    else:
        opts['nfft'] = int(opts['nfft'])
    if not 'cmap' in opts.keys():
        opts['cmap'] = 'BuPu'

    from matplotlib.pyplot import figure, fignum_exists

    i = 1
    while fignum_exists(i):
        i += 1
    fig = figure(i)

    from matplotlib.pyplot import axes
    ax = axes()

    if isinstance(opts['label'], (list, tuple)):
        annotate(*opts['label'], ax=ax)

    noverlap = int(opts['nfft']/2)
    Pxx, fbins, tbins, im = ax.specgram(np.array(x)/(opts['nfft']/2.),
                                        mode='psd', Fs=fs,
                                        NFFT=opts['nfft'], noverlap=noverlap,
                                        cmap=opts['cmap'])
    Pxx = Pxx/np.max(Pxx)
    extent = [tbins.min(), tbins.max(), 0., fbins.max()]

    im = ax.imshow(10*np.log10(Pxx), extent=extent, origin='lower',
                   aspect='auto', cmap=opts['cmap'],
                   vmin=-opts['dynamics'], vmax=0)

    if opts['xlabel'] is not None:
        from matplotlib.pyplot import xlabel
        xlabel(opts['xlabel'])

    if opts['ylabel'] is not None:
        from matplotlib.pyplot import ylabel
        ylabel(opts['ylabel'])

    if opts['title'] is not None:
        from matplotlib.pyplot import title
        title(opts['title'])

    if opts['path'] is not None:
        from matplotlib.pyplot import savefig
        savefig(opts['path'] + '.' + opts['format'])

    fig.colorbar(im, label='Magnitude (dB)')

    if opts['log'] is not None and 'y' in opts['log']:
        from matplotlib.pyplot import yscale
        yscale('log')

    if opts['log'] is not None and 'x' in opts['log']:
        from matplotlib.pyplot import xscale
        xscale('log')

    if show:
        from matplotlib.pyplot import show as pltshow
        pltshow()


def transferFunction(sigin, sigout, fs, nfft=int(2e10), filtering=None,
                     limits=None, noverlap=None):
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

    noverlap : int, optional
        Number of points to overlap between segments. If None, \
noverlap = nperseg // 2. Defaults to None.

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
    f, Pxx_den1 = sig.welch(sigin, fs, nperseg=nfft, scaling='spectrum',
                            noverlap=noverlap)
    f, Pxx_den2 = sig.welch(sigout, fs, nperseg=nfft, scaling='spectrum',
                            noverlap=noverlap)
    TF = Pxx_den2/Pxx_den1
    if limits is not None:
        fmin, fmax = limits
    else:
        fmin, fmax = 0., fs/2.
    nfmax = len(f) if fmax >= f[-1] else np.nonzero(f > fmax)[0][0]
    nfmin = np.nonzero(f >= fmin)[0][0]
    f = np.array(f[nfmin:nfmax])
    TF = np.array(TF[nfmin:nfmax])**0.5
    return f, TF
