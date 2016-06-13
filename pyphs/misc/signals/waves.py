# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 09:29:31 2016

@author: Falaize
"""
_maxVol = 2**15-1.0  # maximum amplitude


def wavread(filename, fs=None, normalize=False):
    """
    read a '.wav' file and return sample rate with data
    Parameters
    ----------

    filename : string or open file handle
        Input wav file.
    mmap : bool, optional
        Whether to read data as memory mapped. Only to be used on real files \
(Default: False)

    Returns
    --------

    rate : int
        Sample rate of wav file
    data : numpy array
        Data read from wav file
    """
    from scipy.io import wavfile
    fs, sig = wavfile.read(filename)
    sig = sig.astype(float)
    for i, el in enumerate(sig):
        sig[i] = el/_maxVol
    return fs, sig


def wavwrite(sig, fs_sig, label, fs_out=None, normalize=None, timefades=0):
    from scipy.signal import resample
    import types

    assert isinstance(sig, (list, types.GeneratorType)), 'Signal should be a \
list or a generator. Got {0!s}'.format(type(sig))
    if isinstance(sig, types.GeneratorType):
        sig = [s for s in sig]

    nsig = len(sig)
    nfades = int(timefades*fs_sig)
    if nsig >= 2*nfades:
        fadein = [n/(nfades) for n in range(nfades)]
        fadeout = [(nfades-1-n)/(nfades) for n in range(nfades)]
        fades = fadein + [1.]*(nsig-2*nfades) + fadeout
        sig = [elsig*elfade for (elsig, elfade) in zip(sig, fades)]

    if fs_out is None:
        fs_out = fs_sig
    sig = resample(sig, int(nsig*fs_out*fs_sig**-1))

    from struct import pack
    import wave
    wv = wave.open(label+'.wav', 'w')
    # nchannels, sampwidth, framerate, nframes, comptype, compname
    wv.setparams((1, 2, fs_out, 0, 'NONE', 'not compressed'))
    if isinstance(normalize, float):
        scale = normalize
    elif isinstance(normalize, bool) and normalize:
        scale = max([abs(el) for el in sig])
    else:
        scale = 1.
    wvData = []
    for i in range(0, sig.__len__()):
        data = int(_maxVol*sig[i]/scale)
        wvData += pack('h', data)
    wv.writeframes(''.join(wvData))
    wv.close()
