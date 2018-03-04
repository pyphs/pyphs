.. title: Port-Hamiltonian Systems
.. slug: port-hamiltonian-systems
.. date: 2017-02-11 18:19:33 UTC+01:00
.. tags: mathjax, theory, phs
.. category: documentation
.. link:
.. description:
.. type: text

In this post, we recall the *port-Hamiltonian systems (PHS)* formalism.
It is shown how this structure guarantees a continuous time power balance, and thus defines a passive system.
**PyPHS** aims at simulating such passive systems by firstly generating the structure equations (5) below associated to a given circuit (graph), and secondly by deriving its numerical version so that a discrete power balance is satisfied.

.. TEASER_END: Read more

The following presentation is adapted from the reference [FH2016]_. This reference is the first corner stone of the PyPHS project, which presents (i) the Port-Hamiltonian Systems (PHS) formalism, (ii) an algorithm for generating the PHS structure associated to a given network by automated graph analysis, and (iii) the structure preserving numerical method for passive guaranteed simulations.
Reference [FH2016] is devoted to the treatment of electronic circuits for which power variables are chosen as current and voltage. However, all the following definitions apply equally to multiphysical systems, provided an adapted set of power variables, generically denoted by flux (currents, velocities, magnetic flux variations) and efforts (voltages, forces, magnetomotive force), the product of which is a power:

+-----------------+-------------------------+-------------------------+
| Domain          | Flux                    | Effort                  |
+=================+=========================+=========================+
| Electronics     | Current (A)             | Voltage (V)             |
+-----------------+-------------------------+-------------------------+
| Mechanics       | Force (N)               | Velocity (m/s)          |
+-----------------+-------------------------+-------------------------+
| Mechanics dual  | Velocity (m/s)          | Force (N)               |
+-----------------+-------------------------+-------------------------+
| Magnetics       | Flux variation (V)      | Magnetomotive Force (A) |
+-----------------+-------------------------+-------------------------+
| Thermics        | Entropy variation (W/K) | Temperature (K)         |
+-----------------+-------------------------+-------------------------+



Power balance
=============

Denote :math:`E(t)\geq 0` the energy *stored* in an open physical system. If the system is conservative, its time variation :math:`\frac{\mathrm d \mathrm E}{\mathrm d t}(t)` reduces to :math:`\mathrm S(t)` the power **received** by the *sources* through the external ports. If the system includes dissipative phenomena, :math:`\mathrm D(t)\geq0` is the *dissipated* power, and the evolution of energy is governed by the following instantaneous **power balance**:

.. math::

	\begin{array}{lr}\frac{\mathrm d \mathrm E}{\mathrm d t}(t) + \mathrm D(t) + \mathrm S(t)=0.  & \qquad\qquad(1)\end{array}

The port-Hamiltonian approach is used to decompose such open physical systems into (i) a set of components that are combined according to (ii) a conservative interconnection network. These two ingredients are detailed below.

Components
==========

The elementary components of multiphysical systems are sorted as (or can be a combination of):

* :math:`n_S` internal components that store energy :math:`\mathrm E \geq 0` (capacitor, inductor, spring, mass, heat capacity, etc.),
* :math:`n_D` internal components that dissipate power :math:`\mathrm D\geq 0` (resistor, diode, damper, etc.),
* :math:`n_P` external ports that convey power :math:`\mathrm S(\in \mathbb R)` from sources (current/voltage source, external force, imposed velocity/temperature, etc.), or any external system (active, dissipative, or mixed).

The behavior of each component is described by a relation between two power variables: the *flux* :math:`f` and the *effort* :math:`e`, defined in **receiver convention** (the *received* power is :math:`\mathrm P=e⋅f`, including for the sources).

Storage components
------------------

The energy :math:`\mathrm E_s` stored in storage component :math:`s\in [1,\,\cdots ,\,n_S]` is expressed as a *storage function* :math:`h_s` of an appropriate state :math:`x_s`: :math:`\mathrm E_s(t)=h_s(x_s(t))\geq 0`.

Example 1:
	For a linear inductor with inductance :math:`L`, the state can be the magnetic flux :math:`x_L=\phi` and the positive definite function is :math:`h_L(\phi)=\phi^2/(2\,L)`.

Example 2:
	For a nonlinear cubic spring with linear stiffness :math:`K` and nonlinearity coefficient :math:`\alpha`, the state can be the ellongation :math:`x_K=\ell` and the positive definite function is :math:`h_K(\ell)=\frac{K}{2}\ell^2\,(1 + \frac{\alpha}{2}\ell^2)`.

Storage power variables (:math:`e_s`, :math:`f_s`) are related to the variation of the state :math:`\frac{\mathrm d x_s}{\mathrm dt}` and the gradient of the storage function :math:`h^\prime _s(x_s)`, the product of which is precisely the received power: :math:`e_s\,f_s=\frac{\mathrm d \mathrm E}{\mathrm d t}=h^\prime _s\,\frac{\mathrm d x_s}{\mathrm d t}`.

Example 1 (continued):
	For the above linear inductor, these constitutive laws are the voltage (effort) :math:`e_L=V_L=\frac{\mathrm d \phi}{\mathrm d t}=\frac{\mathrm d x_L}{\mathrm d t}` and the current (flux) :math:`i_L=\frac{\phi}{L}=h^\prime_L`, the product of which :math:`P_{L}=V_L\,i_L` is the electrical power.

Example 2 (continued):
	For the above nonlinear cubic spring, these constitutive laws are the velocity (flux) :math:`v_K=\frac{\mathrm d \ell}{\mathrm d t}=\frac{\mathrm d x_K}{\mathrm d t}` and the mechanical force (effort) :math:`F_K=K\,(\ell+\alpha\,\ell^3)=h^\prime_K`, the product of which :math:`P_{K}=F_K\,v_K` is the mechanical power (*i.e.* variation of mechanical work).

Finally, the total energy of a system with :math:`n_S` storage components is :math:`\mathrm E =\mathrm H(\mathbf x) = \sum_{i=1}^{N}h_i(x_i)`. The total storage function :math:`\mathrm H: \mathbb R^N \mapsto \mathbb R_{+}` is called the  **Hamiltonian** of the system. Then, the total energy variation of the system is :math:`P_{\mathrm{storage}}=\frac{\mathrm d E}{\mathrm d t} = \nabla \mathrm H \cdot \frac{\mathrm d \mathbf x}{\mathrm d t}= \sum_{i=1}^N \frac{\partial h}{x_i}\,\frac{\mathrm d x_i}{\mathrm d t}`.


*Note that the above definitions can be straightforwardly extended to account for storage components defined by a multivariate storage functions*
:math:`h_s(\mathbf x_s)` with state :math:`\mathbf x_s = (x_{s,1},\,\cdots,\, x_{s,n})^\intercal`
*and associated received power*
:math:`\mathrm P_s = \frac{\mathrm d h_s(\mathbf x_s)}{\mathrm d t} = \nabla h_s \cdot \frac{\mathrm d \mathbf x_s}{\mathrm d t}= \sum_{i=1}^n \frac{\partial h_{s,i}}{x_{s,i}}\,\frac{\mathrm d x_{s,i}}{\mathrm d t}.`

Dissipative components
-----------------------

The power :math:`D_d` instantaneously dissipated by the dissipative component :math:`d\in [1,\,\cdots,\,n_D]` is expressed with respect to an appropriate dissipation variable :math:`w_d`: :math:`D_d(t)\equiv D_d(w_d(t))\geq 0`. Typically, for a linear resistance :math:`R`, :math:`w_R` can be a current :math:`w_R=i_R` and :math:`D_R(i_R)=R⋅i_R^2`.

As for storage components, a mapping of the dissipative power variables (:math:`v_d`, :math:`i_d`) is provided, based on the factorization :math:`D_d(w_d)=w_d\,z_d(w_d)`, introducing a dissipation function :math:`z_d`.
For the resistance, :math:`i_R=w_R` and :math:`V_R=R\,i_R=z_R(w_R)`.

Source components
------------------

The power instantaneously provided to the system through external port
:math:`p \in [1\cdot n_P]`
is
:math:`S_p(t)`
, and we arrange the source variables
:math:`(v_p,i_p)`
in two vectors: one is considered as an input
:math:`u_p`
, and the other as the associated output
:math:`y_p`
, so that the power received from sources on port
:math:`{p}`
is
:math:`S_p=y_p\, u_p=−v_p \,i_p` (receiver convention, with :math:`v_p\,i_p` the power received by the sources).

Conservative Interconnection
============================

The interconnection of the components is achieved by relating all the voltages and currents through the application of the Kirchhoff’s laws to the interconnection network (schematic).
This defines a conservative interconnection, according to Tellegen’s theorem recalled below.

**Tellegen Theorem**:

*Consider an electronic circuit made of*
:math:`{N}`
*edges defined in same convention (here receiver), with individual voltages*
:math:`\mathbf v=(v_1,\cdots,v_N)^\intercal`
*and currents*
:math:`\mathbf i=(i_1,\cdots,i_N)^\intercal`
*which all comply with the Kirchhoff’s laws. Then*

.. math::
		\begin{array}{lr}\mathbf v^\intercal \cdot \mathbf i = 0.  & \qquad\qquad(2)\end{array}


A direct consequence of (2) is that no power is created nor lost in the structure: :math:`\mathbf v^\intercal\cdot\mathbf i=\sum_{i=1}^N P_n=0`, with :math:`P_n = v_n \,i_n ` the power received by edge :math:`n`, thus defining a conservative interconnection (Tellegen’s theorem is a special case of a more general interconnection structure, namely, the Dirac structure).
Now, denote
:math:`(\mathbf v_{\mathrm s},\mathbf i_{\mathrm s})`,
:math:`(\mathbf v_{\mathrm d},\mathbf i_{\mathrm d})`, and
:math:`(\mathbf v_{\mathrm p},\mathbf i_{\mathrm p})`
the sets of all the power variables associated with storage components, dissipative components, and sources (respectively), and
:math:`\mathbf v=(\mathbf v_{\mathrm s}^\intercal,\mathbf v_{\mathrm d}^\intercal,\mathbf v_{\mathrm p}^\intercal)^\intercal`
with
:math:`\mathbf i=(\mathbf i_{\mathrm s}^\intercal,\mathbf i_{\mathrm d}^\intercal,\mathbf i_{\mathrm p}^\intercal)^\intercal`
the vectors of all the power variables.
Then, Tellegen’s theorem restores the power balance (1) with

.. math::
	\begin{array}{lcccr} \mathbf v^\intercal \cdot \mathbf i &=& \mathbf v^\intercal \cdot \mathbf i + \mathbf v^\intercal \cdot \mathbf i + \mathbf v^\intercal \cdot \mathbf i & \\
	& = & \nabla \mathrm H \cdot \frac{\mathrm d \mathbf x}{\mathrm d t} + \mathbf z(\mathbf w)^\intercal \cdot \mathbf w + \mathbf y^\intercal \cdot \mathbf u & = & 0.  & \qquad\qquad(3)\end{array}


where
:math:`\nabla \mathrm H: \mathbb R^{n_S} \rightarrow \mathbb R ^{n_S}`
denotes the gradient of the total energy
:math:`\mathrm E=\mathrm H(\mathbf x)=\sum_{s=1}^{n_S} h_s(x_s)`
with respect to (w.r.t.) the vector of the states
:math:`[\mathbf x]s=x_s`,
and function
:math:`\mathbf z : \mathbb R^{n_D} \rightarrow \mathbb R ^{n_D}`
denotes the collection of functions
:math:`z_d`
w.r.t. the vector
:math:`\mathbf w \in \mathbb R^{n_D}`
of
:math:`[\mathbf w]_d=w_d`
so that
:math:`\mathbf z(\mathbf w)^\intercal ⋅\mathbf w=\sum_{n=1}^{n_D}D_d(w_d)`
is the total dissipated power.

Port-Hamiltonian System
=======================

The above description of storage components, dissipative components, and source, along with the conservative interconnection stated by the Kirchhoff’s laws, constitute the minimal definition of a port-Hamiltonian system (PHS).
In **PyPHS**, we focus on systems that admit an explicit realization of PHS, for which the quantities
:math:`\mathbf b=(b_1,\cdot,b_N)^\intercal=(\frac{\mathrm d \mathbf x^\intercal}{\mathrm d t},\mathbf w^\intercal,−\mathbf y^\intercal)^\intercal`
(with :math:`b_n=v_n` or :math:`b_n=i_n`) can be expressed as linear combinations of the remaining
:math:`{N}`
powers variables organized in the dual vector
:math:`\mathbf a=(a_1,\cdot,a_N)^\intercal=(\nabla \mathrm H(\mathbf x)^\intercal,\mathbf z(\mathbf w)^\intercal,\mathbf u^\intercal)^\intercal`
(with :math:`a_n=i_n` if :math:`b_n=v_n` or :math:`a_n=v_n` if :math:`b_n=i_n`)
:

.. math::
	\begin{array}{lr} \mathbf b = \mathbf J \cdot \mathbf a. & \qquad\qquad(4)\end{array}


Then,
:math:`\mathbf a^\intercal \cdot \mathbf  b=\mathbf a^\intercal⋅\mathbf J\cdot\mathbf a=0`
from Tellegen’s theorem, so that the matrix
:math:`\mathbf J`
is necessarily skew-symmetric (:math:`\mathbf J^\intercal=-\mathbf J`).
More precisely, we consider the following **differential-algebraic system of equations**:

.. math::
	\begin{array}{lr}
	\left(
	\begin{array}{c}
	\frac{\mathrm d \mathbf x}{\mathrm d t}\\
	\mathbf w\\
	\mathbf y
	\end{array}\right)
	=
	\left(
	\begin{array}{lll}
	\mathbf J_{\mathrm{xx}} & \mathbf J_{\mathrm{xw}} & \mathbf J_{\mathrm{xy}} \\
	\mathbf J_{\mathrm{wx}} & \mathbf J_{\mathrm{ww}} & \mathbf J_{\mathrm{wy}} \\
	\mathbf J_{\mathrm{yx}} & \mathbf J_{\mathrm{yw}} & \mathbf J_{\mathrm{yy}} \\
	\end{array}
	\right)
	\cdot
	\left(
	\begin{array}{c}
	\nabla \mathrm H(\mathbf x)\\
	\mathbf z(\mathbf w)\\
	\mathbf u
	\end{array}\right),
	& \qquad\qquad(5)\end{array}


where matrices on the diagonal
:math:`\mathbf J_{\mathrm{xx}}`
,
:math:`\mathbf J_{\mathrm{ww}}`
,
:math:`\mathbf J_{\mathrm{yy}}`
are skew-symmetric.
The significance of the structure matrices is the following:

* :math:`\mathbf J_{\mathrm{xx}}\in\mathbb R^{n_S\times n_S}` expresses the conservative power exchanges between storage components (this corresponds to the so-called :math:`\mathbf J` matrix in classical Hamiltonian systems);

* :math:`\mathbf J_{\mathrm{ww}}\in\mathbb R^{n_D\times n_D}` expresses the conservative power exchanges between dissipative components;

* :math:`\mathbf J_{\mathrm{yy}}\in\mathbb R^{n_P\times n_P}` expresses the conservative power exchanges between ports (direct connections of inputs to outputs);

* :math:`\mathbf J_{\mathrm{xw}}\in\mathbb R^{n_S\times n_D}` expresses the conservative power exchanges between the storage components and the dissipative components;

* :math:`\mathbf J_{\mathrm{xy}}\in\mathbb R^{n_S\times n_P}` expresses the conservative power exchanges between ports and storage components (input gain matrix);

* :math:`\mathbf J_{\mathrm{wy}}\in\mathbb R^{n_D\times n_P}`  expresses the conservative power exchanges between ports and dissipative components (input gain matrix);

* :math:`\mathbf J_{\mathrm{wx}}^\intercal=-\mathbf J_{\mathrm{xw}}`, :math:`\mathbf J_{\mathrm{yx}}^\intercal=-\mathbf J_{\mathrm{xy}}`, :math:`\mathbf J_{\mathrm{yw}}^\intercal=-\mathbf J_{\mathrm{wy}}`.

The PHS (5) fulfills the definition of **passivity** according to the following property.

**Power Balance:**

The variation of the total energy
:math:`\mathrm E=\mathrm H(\mathbf x)`
of a system governed by (5) is given by (1), with
:math:`\mathrm D=\mathbf z(\mathbf w)^\intercal\cdot \mathbf w\geq 0`
the total dissipated power, and
:math:`\mathrm S=\mathbf u^\intercal\cdot \mathbf y`
the total power incoming on external ports.

**Proof:**

We have
:math:`\mathbf a^\intercal\cdot\mathbf b=\frac{\mathrm d\mathrm E}{\mathrm d t}+\mathrm D+\mathrm S.`
Now
:math:`\mathbf a^\intercal\cdot\mathbf b=\mathbf a^\intercal\cdot\mathbf J\cdot\mathbf a=0`
since
:math:`{\mathbf J}`
is skew-symmetric.

**Reduction of the dissipation function:**

Notice the system (5) can be reduced by (i) decomposing the function :math:`\mathbf z`
into its linear and nonlinear parts, and (ii) constructing the **resistive interconnection** associated with its linear part.
Details can be found in appendix of reference [FH2016].

Reference
=========

.. [FH2016] Falaize, A., & Hélie, T. (2016). Passive Guaranteed Simulation of Analog Audio Circuits: A Port-Hamiltonian Approach. Applied Sciences, 6(10), 273.
