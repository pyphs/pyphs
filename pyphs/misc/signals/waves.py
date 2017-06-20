# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 09:29:31 2016

@author: Falaize
"""
from scipy.signal import resample
import types
from struct import pack
from scipy.io import wavfile
import wave


_maxVol = 2**15-1.0  # maximum amplitude


def wavread(path, fs=None, normalize=False):
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
    fs, sig = wavfile.read(path)
    sig = sig.astype(float)
    for i, el in enumerate(sig):
        sig[i] = el/_maxVol
    return fs, sig


def wavwrite(sig, fs_sig, path, fs_out=None, normalize=None, timefades=0):
    assert isinstance(sig, (list, types.GeneratorType)), 'Signal should be a \
list or a generator. Got {0!s}'.format(type(sig))
    if isinstance(sig, types.GeneratorType):
        print('Convert generator to list...')
        sig = list(sig)

    nsig = len(sig)
    nfades = int(timefades*fs_sig)
    if nsig >= 2*nfades:
        fadein = [n/(nfades) for n in range(nfades)]
        fadeout = [(nfades-1-n)/(nfades) for n in range(nfades)]
        fades = fadein + [1.]*(nsig-2*nfades) + fadeout
        print('Fade begining and ending...')
        sig = [elsig*elfade for (elsig, elfade) in zip(sig, fades)]

    if fs_out is None:
        fs_out = fs_sig
    elif not fs_out == fs_sig:
        print('Resampling from {}Hz to {}Hz...'.format(fs_sig, fs_out))
        sig = resample(sig, int(nsig*fs_out*fs_sig**-1))

    if not path.endswith('.wav'):
        path += '.wav'
    wv = wave.open(path, 'w')
    # nchannels, sampwidth, framerate, nframes, comptype, compname
    wv.setparams((1, 2, fs_out, 0, 'NONE', 'not compressed'))
    if isinstance(normalize, float):
        scale = normalize
    elif isinstance(normalize, bool) and normalize:
        scale = max([abs(el) for el in sig])
        if scale == 0:
            scale = 1.
    else:
        scale = 1.
    print('Write wave file...')
    for i, val in enumerate(sig):
        data = int(_maxVol*val/scale)
        wv.writeframes(pack('h', data))
    wv.close()
