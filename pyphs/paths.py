# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:10:39 2016

@author: Falaize
"""


def _init_paths(phs, path):
    """
    set path for PortHamiltonianObject 'phs'.
        * if path is None, no path is used;
        * if path is 'cwd', current working directory is used;
        * if path is 'label', a new folder with phs label is created in \
current working directory;
        * if path is a str, it is used for the system's path.
    """
    import os
    if path is not None:
	    assert isinstance(path, str)
	    # define path
	    if path is 'cwd':
	        phs_path = os.getcwd()
	    elif path is 'label':
	        phs_path = os.getcwd() + os.path.sep + phs.label
	    else:
	        phs_path = path
	    # make dir if not existing
	    if not os.path.exists(phs_path):
	        os.makedirs(phs_path)
	    # Define path for exports (plots, waves, tex, c++, etc...)
	    phs.path = phs_path
	    phs.paths = {'tex': phs_path+os.sep+'tex',
	                 'cpp': phs_path+os.sep+'cpp',
	                 'main': phs_path,
	                 'figures': phs_path+os.sep+'figures',
	                 'data': phs_path+os.sep+'data',
	                 'graph': phs_path+os.sep+'graph'}
