# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 18:56:56 2016

@author: Falaize
"""
from .processing import lowpass
from pyphs.misc.plots.tools import (activate_latex, annotate, setticks, dec,
                               standard)
from pyphs.misc.plots.fonts import globalfonts
import numpy as np


def spectrogram(datax, datay, fs, **kwargs):
    """
    Plot spectrogramm of datay.

    Parameters
    ----------

    datax : list of numerics
        x-axis values.

    datay : list of lists of numerics
        y-axis values for each curve.

    labels : list, optional
        list of curve labels (the default is None).

    unitx : str, optional
        x-axis label (the default is None).

    unity : list of str, optional
        y-axis labels (the default is None).

    ylims : tuple of float, optional
        (ymin, ymax) values. If None then (ymin, ymax) is set automatically \
(the default is None).
        If extend the y-axis is extended by 5% on both sides (the default is \
'extend').

    linewidth : float, optional
        The default is 2.

    figsize : tuple of float, optional
        The default is (5., 5.).

    filelabel : str, optional
        Figure is saved in 'filelabel.png' (the default is 'multiplot').

    loc : int or string or pair of floats, default: 0
        The location of the legend. Possible codes are:

            ===============   =============
            Location String   Location Code
            ===============   =============
            'best'            0
            'upper right'     1
            'upper left'      2
            'lower left'      3
            'lower right'     4
            'right'           5
            'center left'     6
            'center right'    7
            'lower center'    8
            'upper center'    9
            'center'          10
            ===============   =============

    log : str, optional
        Log-scale activation according to
            ===============   =============
            Plot type          Code
            ===============   =============
            'plot'            ''
            'semilogx'        'x'
            'semilogy'        'y'
            'loglog'          'xy'
            ===============   =============

    linestyles : iterable, otpional
        List of line styles; the default is ('-b', '--r', ':g', '-.m').

    fontsize : int, optional
        the default is figsize[0]*4.

    legendfontsize : int, optional
        Figure legend font size. If None then set to 4/5 of fontsize (the \
default is None).

    maintitle : str, optional
        Figure main title. If set to None, the desactivated (the default is \
None).

    axedef : tuple of floats, optional
        Figure geometry (left, botom, right, top).
        The default is (.15, .15, .85, .85).

    nbinsx, nbinsy : int, optional
        number of x-axis and y-axis ticks (the default is 4).

    minor : bool
        Activate the minor grid.

    markersize : float
        Default is 6.

    markeredgewidth : float
        Width of line around markers (the default is 0.5).

    """
    opts = standard.copy()
    opts.update(kwargs)
    if opts['axedef'] is None:
        opts['axedef'] = [.15, .15, .75, .75]
    if opts['linestyles'] is None:
        opts['linestyles'] = ['-b', '--r', '-.g', ':m']
    nplots = int(datay.__len__())
    if opts['fontsize'] is None:
        opts['fontsize'] = int(4*opts['figsize'][0])
    if opts['legendfontsize'] is None:
        opts['legendfontsize'] = int(0.8*opts['fontsize'])
    if opts['labels'] is None:
        opts['labels'] = None
    if opts['log'] is None:
        opts['log'] = ''
    if not 'dynamics' in opts.keys():
        opts['dynamics'] = 80.
    if not 'ylimits' in opts.keys():
        opts['ylimits'] = (10, fs/2.)
    if not 'xlimits' in opts.keys():
        opts['xlimits'] = (datax[0], datax[-1])

    activate_latex(opts)

    from matplotlib.pyplot import rc
    rc('font', size=opts['fontsize'], **globalfonts())

    from matplotlib.pyplot import close
    close('all')

    from matplotlib.pyplot import figure
    fig = figure(1, figsize=opts['figsize'])

    if isinstance(datax[0], (float, int)):
        datax = [datax, ]*nplots

    from matplotlib.pyplot import axes
    ax = axes(opts['axedef'][:4])

    miny = float('Inf')
    maxy = -float('Inf')

    x = dec(datax, opts)
    y = dec(datay, opts)
    maxy = max([maxy, max(y)])
    miny = min([miny, min(y)])

    if isinstance(opts['labels'], (list, tuple)):
        annotate(x, y, opts['labels'][0], opts['labels'][1],
                 opts['legendfontsize'])

    noverlap = int(opts['nfft']/2)
    Pxx, fbins, tbins, im = ax.specgram(np.array(y)/(opts['nfft']/2),
                                        mode='psd', Fs=fs,
                                        NFFT=opts['nfft'], noverlap=noverlap,
                                        cmap=opts['colormap'])
    Pxx = Pxx/np.max(Pxx)
    extent = [tbins.min(), tbins.max(), fbins.min(), fbins.max()]
    im = ax.imshow(10*np.log10(Pxx), extent=extent, origin='lower',
                   aspect='auto', cmap=opts['colormap'],
                   vmin=-opts['dynamics'], vmax=0)

    setticks(ax, opts)

    ax.set_ylim(opts['ylimits'])
    ax.set_xlim(opts['xlimits'])

    if opts['unitx'] is not None:
        from matplotlib.pyplot import xlabel
        xlabel(opts['unitx'])

    if opts['unity'] is not None:
        from matplotlib.pyplot import ylabel
        ylabel(opts['unity'])

    if opts['maintitle'] is not None:
        from matplotlib.pyplot import title
        title(opts['maintitle'])

    if opts['filelabel'] is not None:
        from matplotlib.pyplot import savefig
        savefig(opts['filelabel'] + '.' + opts['format'])

    ax.yaxis.set_label_coords(opts['xpos_ylabel'], 0.5)

    cbar_ax = fig.add_axes([0.87, 0.397, 0.01, 0.555])
    fig.colorbar(im, cax=cbar_ax, label='Magnitude (dB)')

    
def transferFunction(sigin, sigout, fs, nfft=int(2e13), filtering=None,
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
