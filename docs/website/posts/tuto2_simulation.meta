.. title: Building of the RLC circuit
.. slug: RLC
.. date: 2016-11-05 16:30:33 UTC+02:00
.. tags: mathjax
.. link: 
.. description: 
.. type: text
.. author: Antoine Falaize

The basic use of the *pyphs.PortHamiltonianObject* is illustrated here
with the modeling of the standard reistor-inductor-capacitor (RLC)
circuit given by (see `[1,
§2.2] <http://www.mdpi.com/2076-3417/6/10/273/pdf>`__):

.. math::

   \left(\begin{array}{c}\frac{\mathrm d x_L}{\mathrm d  t} \\ \frac{\mathrm d x_C}{\mathrm d  t}\\ \hline w_R\\ \hline y \end{array}\right)=\left(\begin{array}{cc|c|c}
   0 & -1 & -1 & -1\\ 
   1 & 0 & 0 & 0 \\ \hline
   1 & 0 & 0 & 0 \\  \hline
   1 & 0 & 0 & 0
   \end{array}\right)\cdot \left(\begin{array}{c}\frac{\partial H}{\partial x_C}\\ \frac{\partial H}{\partial x_L}\\ \hline z_R\\ \hline u \end{array}\right) 

 The constitutive laws are: \* the quadratic storage function
:math:`H(x_L, x_C)=\frac{x_L^2}{2L}+\frac{x_C^2}{2C},` \* the linear
dissipation funciton :math:`z_R(w_R)= R \,w_R.`

The physical parameters are \* :math:`C=2\times 12^{-9}`\ F, \*
:math:`L=50\times 10^{-3}`\ H, \* :math:`R = 10^3\Omega`.

.. code:: python

    import pyphs
    
    rlc = pyphs.PortHamiltonianObject(label='RLC')

.. code:: python

    x, L = rlc.symbols(['xL', 'L'])
    h = x**2/(2*L)
    
    rlc.add_storages(x, h)
    
    L_value = 5e-3
    rlc.symbs.subs.update({L:L_value})

.. code:: python

    xC, C = rlc.symbols(['xC', 'C'])
    H = xC**2/(2*C)
    
    rlc.add_storages(xC, H)
    
    C_value = 2e-9
    rlc.symbs.subs.update({C:C_value})

.. code:: python

    w, par_symb = rlc.symbols(['wR', 'R'])
    par_value = 1e3
    
    z = par_symb*w
    rlc.add_dissipations(w, z)
    rlc.symbs.subs.update({par_symb:par_value})

.. code:: python

    u, y = rlc.symbols(['v', 'i'])
    rlc.add_ports(u, y)

.. code:: python

    import numpy
    rlc.struc.set_Mxx(numpy.array([[0, -1], [1, 0]]))
    rlc.struc.set_Mxw(numpy.array([[-1], [0]]))
    rlc.struc.set_Mxy(numpy.array([[-1], [0]]))
    rlc.struc.set_Mwx(numpy.array([[1, 0]]))
    rlc.struc.set_Myx(numpy.array([[1, 0]]))

.. code:: python

    rlc.symbs.x




.. parsed-literal::

    [xL, xC]



.. code:: python

    rlc.exprs.H




.. parsed-literal::

    xL**2/(2*L) + xC**2/(2*C)



.. code:: python

    rlc.symbs.w




.. parsed-literal::

    [wR]



.. code:: python

    rlc.exprs.z




.. parsed-literal::

    [R*wR]



.. code:: python

    rlc.symbs.subs




.. parsed-literal::

    {C: 2e-09, R: 1000.0, L: 0.005}



.. code:: python

    rlc.struc.M




.. parsed-literal::

    Matrix([
    [0, -1, -1, -1],
    [1,  0,  0,  0],
    [1,  0,  0,  0],
    [1,  0,  0,  0]])



.. code:: python

    rlc.struc.J()




.. parsed-literal::

    Matrix([
    [  0, -1.0, -1.0, -1.0],
    [1.0,    0,    0,    0],
    [1.0,    0,    0,    0],
    [1.0,    0,    0,    0]])



.. code:: python

    rlc.struc.Jxx()




.. parsed-literal::

    Matrix([
    [  0, -1.0],
    [1.0,    0]])



.. code:: python

    rlc.struc.Jxw()




.. parsed-literal::

    Matrix([
    [-1.0],
    [   0]])



.. code:: python

    rlc.struc.Jwx() + rlc.struc.Jxw().T




.. parsed-literal::

    Matrix([[0, 0]])



.. code:: python

    rlc.struc.R()




.. parsed-literal::

    Matrix([
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]])



.. code:: python

    rlc.build_resistive_structure()

.. code:: python

    rlc.struc.M




.. parsed-literal::

    Matrix([
    [-R, -1, -1],
    [ 1,  0,  0],
    [ 1,  0,  0]])



.. code:: python

    rlc.struc.J()




.. parsed-literal::

    Matrix([
    [  0, -1.0, -1.0],
    [1.0,    0,    0],
    [1.0,    0,    0]])



.. code:: python

    rlc.struc.R()




.. parsed-literal::

    Matrix([
    [1.0*R, 0, 0],
    [    0, 0, 0],
    [    0, 0, 0]])



.. code:: python

    rlc.symbs.w




.. parsed-literal::

    []



.. code:: python

    rlc.exprs.z




.. parsed-literal::

    []



