# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 12:59:17 2016

@author: Falaize
"""

def plotprops(which='single'):
    if which=='single':
        return {                       
       'loc':1,
       'linestyles':['-','--s',':o','-.D'],
       'markeredgewidth': 1,
       'axedef': (0.15, 0.15, 0.75, 0.75),
       'markersize':8,
        'linewidth':2, 
        'figsize':(7., 6.),
        'nbinsx':5, 
        'nbinsy':5,
        'minor':True}
    if which=='multi':
        return {                       
        'legendfontsize':None, 
        'linewidth':2, 
        'figsize':(7., 6.),
        'loc':0, 
        'linestyles':('-b', '--r', ':g', '-.m'), 
        'axedef':(.15, .15, .85, .85, .1, .3),
        'nbinsx':6, 
        'nbinsy':5,
        'markersize':6, 
        'markeredgewidth':0.5,
        'minor':False}

def font_lists():
    lis = list()
    lis.append(('serif', ['Times', 'Bitstream Vera Serif', 'New Century Schoolbook', 'Century Schoolbook L', 'Utopia', 'ITC Bookman', 'Bookman', 'Nimbus Roman No9 L', 'Times New Roman', 'Palatino', 'Charter', 'Computer Modern', 'serif'],))
    lis.append(('sans-serif', ['Bitstream Vera Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif'],))
    lis.append(('cursive', ['Apple Chancery', 'Textile', 'Zapf Chancery', 'Sand', 'Script MT', 'Felipa', 'cursive'],))
    lis.append(('fantasy', ['Comic Sans MS', 'Chicago', 'Charcoal', 'Impact', 'Western', 'Humor Sans', 'fantasy'],))
    lis.append(('monospace', ['Bitstream Vera Sans Mono', 'Andale Mono', 'Nimbus Mono L', 'Courier New', 'Courier', 'Fixed', 'Terminal', 'monospace'],))
    return lis
    
    return lis
def latex_preamble():
    # Path for latex compiler
    import os
    os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin'
    # Activate use of latex expressions
    from matplotlib.pyplot import rc
    rc('text', usetex=True)
    from matplotlib import rcParams    
    rcParams['text.latex.preamble'] = [' ', ]
#    [
#                                       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
#                                       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
#                                       r'\usepackage{helvet}',    # set the normal font here
#                                       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
#                                       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
#                                       ]  
def Globalfont():
    font_properties = {'family': 'serif',
                        'weight' : 'normal',          
                        'variant':'small-caps'}
    for fonts in font_lists():
        font_properties[fonts[0]] = fonts[1]
    return font_properties

def annotate(x, y, pos, annote, legendfontsize):
    from matplotlib.pyplot import text
    nbin = int(pos*len(x))
    binx = x[nbin]
    biny = y[nbin]
    text(binx, biny, annote, fontdict={'fontsize': legendfontsize},\
         bbox=dict(facecolor='white', alpha=1.), \
         horizontalalignment='center', verticalalignment='center')

def setticks(ax, ticks_properties):

    major_linewidth = ticks_properties['linewidth']
    minor_linewidth = major_linewidth/4.
    
    from matplotlib.ticker import ScalarFormatter
    majorformatter = ScalarFormatter(useOffset=False)

    from matplotlib.ticker import MaxNLocator, AutoMinorLocator, AutoLocator

    nbinsx = ticks_properties['nbinsx'] + 1
    nbinsy = ticks_properties['nbinsy'] + 1

    if ticks_properties['islog'] == '':
        locatorxMaj = MaxNLocator(nbins=nbinsx)
        locatoryMaj = MaxNLocator(nbins=nbinsy)
        locatorxMin = AutoMinorLocator()
        locatoryMin = AutoMinorLocator()

    elif ticks_properties['islog'] == 'x':
        locatorxMaj = AutoLocator()
        locatoryMaj = MaxNLocator(nbins=nbinsy)
        locatorxMin = locatorxMaj
        locatoryMin = AutoMinorLocator()

    elif ticks_properties['islog'] == 'y':
        locatorxMaj = MaxNLocator(nbins=nbinsx)
        locatoryMaj = AutoLocator()
        locatorxMin = AutoMinorLocator()
        locatoryMin = locatoryMaj

    elif ticks_properties['islog'] == 'xy':
        locatorxMaj = AutoLocator()
        locatoryMaj = AutoLocator()
        locatorxMin = locatorxMaj
        locatoryMin = locatoryMaj

    locatorxMaj = MaxNLocator(nbins=nbinsx)
    locatoryMaj = MaxNLocator(nbins=nbinsy)
            
    # x-axis:
    ax.xaxis.set_major_formatter(majorformatter)
    ax.xaxis.set_major_locator(locatorxMaj)

    # y-axis
    ax.yaxis.set_major_formatter(majorformatter)
    ax.yaxis.set_major_locator(locatoryMaj)

    # grid
    ax.xaxis.grid(True,'major',linewidth=major_linewidth)
    ax.yaxis.grid(True,'major',linewidth=major_linewidth)
    if ticks_properties['minor']:
        ax.xaxis.set_minor_locator(locatorxMin)
        ax.yaxis.set_minor_locator(locatoryMin)
        ax.xaxis.grid(True,'minor', linewidth=minor_linewidth)
        ax.yaxis.grid(True,'minor', linewidth=minor_linewidth)

    ax.ticklabel_format(axis='both', style='sci', scilimits=(-2, 2))    
    ax.tick_params(axis='both', labelsize=ticks_properties['ticksfontsize'])
    t = ax.xaxis.get_offset_text()
    t.set_size(ticks_properties['ticksfontsize'])    
    t = ax.yaxis.get_offset_text()
    t.set_size(ticks_properties['ticksfontsize'])    
    

def setlims(ax, x, miny, maxy, limy):
    limx = (min(x), max(x))
    ax.set_xlim(limx)        
    if limy is None:
        limy = (float(miny), float(maxy))
    elif limy == 'extend':
        extend = 0.05
        rangey = maxy-miny
        limy = (float(miny-rangey*extend), float(maxy+rangey*extend))
    ax.set_ylim(limy)        

def whichplot(which, axe):
    if which == '':
        return axe.plot
    elif which == 'x':
        return axe.semilogx
    elif which == 'y':
        return axe.semilogy
    elif which == 'xy':
        return axe.loglog

def multiplot(datax, datay, unitx='', unity=None, labels=None, limits='extend', fontsize=None, \
            legendfontsize=None, linewidth=2, figsize=(7., 6.), \
            filelabel=None, maintitle=None, loc=1, log=None, \
            linestyles=('-b', '--r', ':g', '-.m'), axedef=(.15, .15, .85, .85, .1, .3), \
            nbinsx=4, nbinsy=4, minor=True, xpos_ylabel=None, markersize=6, markeredgewidth=0.5, maxnplot=float('Inf')):
    """
    Plot multiple y-axis and possible multiple curves in each. Result is saved as a '.png' document.

    Parameters
    ----------    
    
    datax : list of floats
        x-axis values.
    
    datay : list of floats or list of tuples of list of floats
        y-axis values per axis and per curve in each axis, if tuple.

    labels : list, optional
        list of or tupple of list of curve labels (the default is None).

    unitx : str, optional
        x-axis label (the default is None). 

    unity : list of str, optional
        y-axis labels per axis (the default is None).

    limits= : list of tuples, optional
        List of (ymin, ymax) values. If None then (ymin, ymax) is set automatically.
        If 'extend', the y-axis is extend by 5% on both ends (the default is 'extend').

    linewidth : float, optional 
        The default is 2.

    figsize : tuple of float, optional 
        The default is (5., 5.).

    filelabel : str, optional
        Figure is saved in 'filelabel.png' if provided (the default is None).

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
    
    log : list of str, optional
        Log-scale activation for each axis according to 
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
        the default is figsize[0]*4

    legendfontsize : int, optional
        Figure legend font size. If None then set to 4/5 of fontsize (the default is None).

    maintitle : str, optional
        Figure main title. If set to None, the desactivated (the default is None).
    
    axedef : tuple of floats, optional 
        Figure geometry (left, botom, right, top, height, width).
        The default is (.15, .15, .85, .85, .1, .3).

        ======   ===============================================================
        Value    Description
        ======   ===============================================================
        left     the left side of the subplots of the figure.        
        bottom   the bottom of the subplots of the figure.
        right    the right side of the subplots of the figure.
        top      the top of the subplots of the figure.
        wspace   the amount of width reserved for blank space between subplots.
        hspace   the amount of height reserved for white space between subplots.
        ======   ===============================================================
    
    markersize : float
        Default is 6.

    markeredgewidth : float
        Width of line around markers (the default is 0.5).

    nbinsx, nbinsy : int, optional
        number of x-axis and y-axis ticks (the default is 4).

    minor : bool
        Activate the minor grid.
        
    xpos_ylabel : float, optional
        If provided, set the x-position of the ylabels so that they align (the default is None).
        You probably want it to be negative.
        
    """

    nplots = int(datay.__len__())
    if fontsize is None: fontsize = int(6*figsize[0])
    if legendfontsize is None: legendfontsize = int(0.8*fontsize)
    if unity is None: unity = ['', ]*nplots
    if limits is None: 
        limits = [None, ]*nplots
    elif limits=='extend':
        limits = ['extend', ]*nplots        
    if labels is None: labels = [None, ]*nplots
    if log is None: log = ['']*nplots

    from matplotlib.pyplot import subplots, close
    close('all')
    fig, axs = subplots(nplots, 1, sharex=True, figsize=figsize)
    
    latex_preamble()    

    # Dic of font properties
    from matplotlib.pyplot import rc
    rc('font', size=fontsize, **Globalfont())

    from misc.tools import decimate
    dec = lambda li: [el for el in decimate(li, max((1, int(len(li)/maxnplot))))]
    x = dec(datax)
            
    for n in range(nplots):

        miny = float('Inf')
        maxy = -float('Inf')

        which_log = log[n]
        
        if type(datay[n]) is list:
            y = dec(datay[n])
            maxy = max([maxy, max(y)])
            miny = min([miny, min(y)])
            plotn = whichplot(which_log, axs[n]) if nplots>1 else whichplot(which_log, axs)
            plotn(x, y, linestyles[0], label=labels[n], linewidth=linewidth, \
                markeredgewidth=markeredgewidth, markersize=markersize)
            
        elif isinstance(datay[n], tuple):
            len_yn = len(datay[n])
            if labels[n] is None: labels[n] = (None, )*len_yn
            for m in range(len_yn):

                if isinstance(labels[n][m], (list, tuple)):
                    annotate(x, y, labels[n][m][0], labels[n][m][1],\
                             legendfontsize)
                    l = None
                else:
                    l = labels[n][m]
                    
                y = dec(datay[n][m])
                maxy = max([maxy, max(y)])
                miny = min([miny, min(y)])
                plotn = whichplot(which_log, axs[n])
                plotn(x, y, linestyles[m], label=l, linewidth=linewidth, \
                markeredgewidth=markeredgewidth, markersize=markersize)

        setlims(axs[n], x, miny, maxy, limits[n])
        ticks_properties = {'linewidth' : linewidth,
                            'nbinsx' : nbinsx,
                            'nbinsy' : nbinsy,
                            'islog' : which_log,
                            'minor' : minor,
                            'ticksfontsize':legendfontsize}
        setticks(axs[n], ticks_properties)
        
        axs[n].legend(loc=loc, fontsize=legendfontsize)
        if not unity[n] is None:
            axs[n].set_ylabel(unity[n], fontsize=fontsize)
            if not xpos_ylabel is None:
                axs[n].yaxis.set_label_coords(xpos_ylabel, 0.5)
        if n == nplots-1:
            axs[n].set_xlabel(unitx, fontsize=fontsize)
        else:
            from matplotlib.pyplot import setp
            setp(axs[n].get_xticklabels(), visible=False)

    if maintitle is not None:
        from matplotlib.pyplot import suptitle
        suptitle(maintitle)

    #fig.tight_layout() # solve overlaping plots
    fig.subplots_adjust(left=axedef[0], bottom=axedef[1], right=axedef[2], \
                        top=axedef[3], wspace=axedef[4], hspace=axedef[5])   

    if not filelabel is None:
        from matplotlib.pyplot import savefig
        savefig(filelabel + '.png')

    from matplotlib.pyplot import show
    show()

def singleplot(datax, datay, labels=None, unitx=None, unity=None, ylims='extend', fontsize=None, \
            legendfontsize=None, linewidth=2, figsize=( 6., 6.), axedef=None, \
            filelabel=None, maintitle=None, loc=1, log='', \
            linestyles=None, nbinsx=4, nbinsy=4, minor=True, markersize=6, markeredgewidth=0.5, maxnplot=float('Inf')):
    """
    Plot multiple y-axis and possible multiple curves in each. Result is saved as a '.png' document.

    Parameters
    ----------
    
    
    datax : list of floats
        x-axis values.
    
    datay : list of list of floats
        y-axis values per curve.

    labels : list, optional
        list of curve labels (the default is None).

    unitx : str, optional
        x-axis label (the default is None). 

    unity : list of str, optional
        y-axis labels (the default is None).

    ylims : tuple of float, optional
        (ymin, ymax) values. If None then (ymin, ymax) is set automatically (the default is None).
        If extend the y-axis is extended by 5% on both sides (the default is 'extend').

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
        Figure legend font size. If None then set to 4/5 of fontsize (the default is None).

    maintitle : str, optional
        Figure main title. If set to None, the desactivated (the default is None).
    
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
    if axedef is None:
        axedef = [.15, .15, .75, .75]
    if linestyles is None:
        linestyles = ['-b','--r',':g','-.m']
    nplots = int(datay.__len__())
    if fontsize is None: fontsize = int(4*figsize[0])
    if legendfontsize is None: legendfontsize = int(0.8*fontsize)
    if labels is None: labels = [None, ]*nplots
    if log is None: log = ['']*nplots

    latex_preamble()    

    from matplotlib.pyplot import rc
    rc('font', size=fontsize, **Globalfont())

    from matplotlib.pyplot import close
    close('all')

    from matplotlib.pyplot import figure
    figure(1,figsize=figsize)
    nplots = datay.__len__()

    if isinstance(datax[0], (float, int)):
        datax = [datax, ]*nplots

    from matplotlib.pyplot import axes
    ax = axes(axedef[:4])

    miny = float('Inf')
    maxy = -float('Inf')

    from misc.tools import decimate
    dec = lambda li: [el for el in decimate(li, max((1, int(len(li)/maxnplot))))]

    for n in range(nplots):

        x = dec(datax[n])
        y = dec(datay[n])
        maxy = max([maxy, max(y)])
        miny = min([miny, min(y)])

        if isinstance(labels[n], (list, tuple)):
            annotate(x, y, labels[n][0], labels[n][1],\
                     legendfontsize)
            l = None
        else:
            l = labels[n]            

        plotn = whichplot(log, ax)
        plotn(x,y,linestyles[n],linewidth=linewidth, markeredgewidth=markeredgewidth,\
        markersize=markersize, label=l)

    setlims(ax, x, miny, maxy, ylims)
    ticks_properties = {'linewidth':linewidth,
                        'nbinsx':nbinsx,
                        'nbinsy':nbinsy,
                        'islog':log,
                        'minor':minor,
                        'ticksfontsize':legendfontsize}
    setticks(ax, ticks_properties)
    
    from matplotlib.pyplot import legend
    legend(loc=loc, fontsize=legendfontsize)

    if not unitx is None:
        from matplotlib.pyplot import xlabel
        xlabel(unitx)

    if not unity is None:
        from matplotlib.pyplot import ylabel
        ylabel(unity)

    if not maintitle is None:
        from matplotlib.pyplot import title
        title(maintitle)

    if not filelabel is None:    
        from matplotlib.pyplot import savefig
        savefig(filelabel + '.png')

    from matplotlib.pyplot import show
    show()


def test_fonts():
    import numpy as np
    t = list(1+np.linspace(0,1, 2000))
    s1 = [2*np.sin(2*np.pi*3*elt) for elt in t]
    s2 = [np.sin(2*np.pi*4*elt) for elt in t]
    Nplot = 2
    datax = t
    datay = [(s1, s2), ]*Nplot
    lab = [None,]*Nplot
    lab[0] = (0.5, r'5Hz')
    lab[1] = (0.25, r'7Hz')

    labels = list()
    labels.append((r'5Hz', r'7Hz'))
    labels.append(lab)
    labels = list()
    labels.append((r'5Hz', r'7Hz'))
    labels.append(lab)
    plot_properties = {'unitx':r'Impedance $\frac{v_\mathtt{I}}{i_\mathtt{I}}$ ($\Omega$=V/A)', 
               'unity':(r'$\sum_{i=1}^n\beta_i$', r'Integral $\int_0^{x_i} f(\alpha) \mathtt{d}$ (V)'),
               'labels':labels, 
               'limits': 'extend',
               'fontsize':20,
               'legendfontsize':None, 
               'linewidth':2, 
               'figsize':(8., 8.),
               'loc':1, 
               'log':('y','x'),
               'linestyles':('-b', '--r', ':g', '-.m'), 
               'axedef':(.15, .15, .85, .85, .1, .3), 
               'nbinsx':4, 
               'nbinsy':4,
               'minor':True}

    for (family, fonts) in font_lists():
        for font in fonts:
            global Globalfont
            def Globalfont():
                # serif fonts: Times, Palatino, New Century Schoolbook, Bookman, Computer Modern, Roman
                # sans-serif fonts: Helvetica, Avant Garde, Computer Modern, Sans serif
                return {'family': family,
                        family: [font],
                        'weight' : 'normal',          
                        'variant':'small-caps',
            }
            import os
            plot_properties['maintitle'] = family+': '+font+r'; $\sum_{i=1}^n\int_0^{x_i} f(\alpha) \mathtt{d}\beta$'
            plot_properties['filelabel'] = 'fonts'+os.sep+family+'_'+font
            multiplot(datax, datay, **plot_properties)    





if __name__ == '__main__':
    import numpy as np
    f0 = 100
    t = list(1/2.+np.linspace(0,1, 2000))
    s1 = [2*np.sin(2*np.pi*3*elt) for elt in t]
    s2 = [np.sin(2*np.pi*4*elt) for elt in t]
    Nplot = 2
    datax = t
    datay = [(s1, s2), ]*Nplot
    lab = [None,]*Nplot
    lab[0] = (0.5, r'5Hz')
    lab[1] = (0.25, r'7Hz')

    labels = list()
    labels.append((r'5Hz', r'7Hz'))
    labels.append(lab)
    plot_properties = {'unitx':'', 
                       'unity':(r'yo $yo$', r'yo $2\,yo=3$'),
                       'labels':labels, 
                       'limits': 'extend',
                       'fontsize':20,
                       'legendfontsize':None, 
                       'linewidth':2, 
                       'figsize':(8., 8.),
                       'filelabel':None, 
                       'maintitle':None, 
                       'loc':1, 
                       'log':('y','x'),
                       'linestyles':('-b', '--r', ':g', '-.m'), 
                       'axedef':(.15, .15, .85, .85, .1, .3), 
                       'nbinsx':20, 
                       'nbinsy':4,
                       'minor':True}
    multiplot(datax, datay, **plot_properties)    
    datay = [s1, s2]
    labels = [r'5Hz', r'7Hz']
    labels[0] = (0.45, r'5Hz')
    labels[-1] = (0.25, r'7Hz')
    datax = t
    plot_properties = {
                       'labels' : None, 
                       'unitx' : None, 
                       'unity' : None, 
                       'ylims' : 'extend', 
                       'fontsize' : 30, 
                       'legendfontsize' : None, 
                       'linewidth' : 2, 
                       'figsize' : ( 6., 6.),
                       'axedef' : [.15, .15, .75, .75], 
                       'filelabel' : None, 
                       'maintitle' : None, 
                       'loc' : 1, 
                       'log' : '', 
                       'linestyles' : ['-b','--r',':g','-.m'], 
                       'nbinsx' : 4, 
                       'nbinsy' : 4,
                       'minor':False}
    #singleplot(datax, datay, **plot_properties)
    #test_fonts()