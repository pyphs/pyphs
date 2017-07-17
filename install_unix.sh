conda_deps='pip libgfortran cython numpy scipy networkx matplotlib nose sympy==1.0 theano'
conda install $conda_deps
pip_deps='stopit progressbar2 nose nose-exclude codecov coveralls'
pip install $pip_deps
pip install -e .
