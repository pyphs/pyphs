.. title: Port-Hamiltonian Systems
.. slug: port-hamiltonian-systems
.. date: 2017-02-11 18:19:33 UTC+01:00
.. tags: mathjax, theory
.. category: tutorial
.. link: 
.. description: 
.. type: text

In this tutorial, we recall the *port-Hamiltonian systems (PHS)* formalism in section 1, and we give an example with the standard serial resistor-coil-capacitor (RLC) circuit in section 2.

.. TEASER_END: click to read the rest of the article

The following presentation is adapted from the reference [FH2016]_.

----------

1 Formalism and properties
===========================

Denote :math:`E(t)\geq 0` the energy *stored* in an open physical system. If the system is conservative, its time variation :math:`\frac{\mathrm d \mathrm E}{\mathrm d t}(t)` reduces to :math:`\mathrm S(t)` the power **received** by the *sources* through the external ports. If the system includes dissipative phenomena, :math:`\mathrm D(t)\geq0` is the *dissipated* power, and the evolution of energy is governed by the following instantaneous **power balance**:

.. math::
	
	\begin{array}{lr}\frac{\mathrm d \mathrm E}{\mathrm d t}(t) + \mathrm D(t) + \mathrm S(t)=0.  & \qquad\qquad(1)\end{array}

The port-Hamiltonian approach is used to decompose such open physical systems into (i) a set of components that are combined according to (ii) a conservative interconnection network. These two ingredients are detailed below.

1.1. Components
------------------------------

The elementary components of multiphysical systems are sorted as (or can be a combination of):

* :math:`n_S` internal components that store energy :math:`\mathrm E \geq 0` (capacitor, inductor, spring, mass, heat capacity, etc.),
* :math:`n_D` internal components that dissipate power :math:`\mathrm D\geq 0` (resistor, diode, damper, etc.),
* :math:`n_P` external ports that convey power :math:`\mathrm S(\in \mathbb R)` from sources (current/voltage source, external force, imposed velocity/temperature, etc.), or any external system (active, dissipative, or mixed).

The behavior of each component is described by a relation between two power variables: the *flux* :math:`f` and the *effort* :math:`e`, defined in **receiver convention** (the *received* power is :math:`\mathrm P=e⋅f`, including for the sources).

Storage components
~~~~~~~~~~~~~~~~~~~

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


	Note the above definitions can be straightforwardly extended to account for storage components defined by a multivariate storage functions :math:`h_s(\mathbf x_s)` with state :math:`\mathbf x_s = (x_{s,1},\,\cdots,\, x_{s,n})^\intercal` and associated received power :math:`\mathrm P_s = \frac{\mathrm d h_s(\mathbf x_s)}{\mathrm d t} = \nabla h_s \cdot \frac{\mathrm d \mathbf x_s}{\mathrm d t}= \sum_{i=1}^n \frac{\partial h_{s,i}}{x_{s,i}}\,\frac{\mathrm d x_{s,i}}{\mathrm d t}`.

Dissipative components
~~~~~~~~~~~~~~~~~~~~~~~~~~

The power :math:`D_d` instantaneously dissipated by the dissipative component :math:`d\in [1,\,\cdots,\,n_D]` is expressed with respect to an appropriate dissipation variable :math:`w_d`: :math:`D_d(t)\equiv D_d(w_d(t))\geq 0`. Typically, for a linear resistance :math:`R`, :math:`w_R` can be a current :math:`w_R=i_R` and :math:`D_R(i_R)=R⋅i_R^2`. 

As for storage components, a mapping of the dissipative power variables (:math:`v_d`, :math:`id`) is provided, based on the factorization :math:`D_d(w_d)=w_d\,z_d(w_d)`, introducing a dissipation function :math:`z_d`. 
For the resistance, :math:`i_R=w_R` and :math:`V_R=R\,i_R=z_R(w_R)`.

Source components
~~~~~~~~~~~~~~~~~~~

The power instantaneously provided to the system through external port p∈[1⋯nP]
is Sp(t), and we arrange the source variables (vp,ip) in two vectors: one is considered as an input up, and the other as the associated output yp, so that the power received from sources on port p is Sp=yp⋅up=−vp⋅ip (receiver convention, with vp⋅ip
the power received by the sources).

Conservative Interconnection
------------------------------

The interconnection of the components is achieved by relating all the voltages and currents through the application of the Kirchhoff’s laws to the interconnection network (schematic). This defines a conservative interconnection, according to Tellegen’s theorem recalled below (see also [26] and [27] §9.4).
Theorem 1 (Tellegen). Consider an electronic circuit made of N edges defined in same convention (here receiver), with individual voltages v=(v1,⋯,vN)⊺
and currents in=(i1,⋯,iN)⊺ which comply with the Kirchhoff’s laws. Then
v⊺⋅i=0.
(2)
A direct consequence of (2) is that no power is created nor lost in the structure: v⊺⋅i=∑Ni=1Pn=0
, with Pn=vn⋅in the power received by edge n, thus defining a conservative interconnection (Tellegen’s theorem is a special case of a more general interconnection structure, namely, the Dirac structure (see [23] §2.1.2 for details)). Now, denote (vs,is), (vd,id), and (vp,ip) the sets of all the power variables associated with storage components, dissipative components, and sources (respectively), and v=(v⊺s,v⊺d,v⊺p)⊺, i=(i⊺s,i⊺d,i⊺p)⊺ the vectors of all the power variables. Then, Tellegen’s theorem restores the power balance (1) with
v⊺⋅i==v⊺s⋅is+v⊺d⋅id+v⊺p⋅ip∇H⊺(x)⋅dxdtdEdt+z(w)⊺⋅wD−u⊺⋅yS,
(3)
where ∇H:RnS→RnS denotes the gradient of the total energy E=H(x)=∑nSs=1hs(xs) with respect to (w.r.t.) the vector of the states [x]s=xs, and function z:RnD→RnD denotes the collection of functions zd w.r.t. the vector w∈RnD of [w]d=wd so that z(w)⊺⋅w=∑nDd=1Dd(wd)
is the total dissipated power.
The above description of storage components, dissipative components, and source, along with the conservative interconnection stated by the Kirchhoff’s laws, constitute the minimal definition of a port-Hamiltonian system (PHS) (see [23] §2.2). In this work, we focus on circuits that admit an explicit realization of PHS, for which the quantities b=(b1,⋯,bN)⊺=(dxdt,w,−y)⊺
(with bn=vn or bn=in) can be expressed as linear combinations of the remaining N powers variables organized in the dual vector a=(a1,⋯,aN)⊺=(∇H(x),z(w),u)⊺ (with an=in if bn=vn or an=vn if bn=in):
b=J⋅a.
(4)
Then, a⊺⋅b=a⊺⋅J⋅a=0
from Tellegen’s theorem, so that the matrix J is necessarily skew-symmetric (J⊺=−J). More precisely, we consider the following algebraic-differential system of equations
⎛⎝⎜⎜dxdtw−y⎞⎠⎟⎟b=⎛⎝⎜⎜JxK⊺Gx⊺−KJwGw⊺−Gx−GwJy⎞⎠⎟⎟J⋅⎛⎝⎜⎜∇H(x)z(w)u⎞⎠⎟⎟a,
(5)
where matrices Jx, Jw, Jy are skew-symmetric. The significance of the structure matrices is the following:

Jx∈RnS×nS

    expresses the conservative power exchanges between storage components (this corresponds to the so-called J
    matrix in classical Hamiltonian systems);
Jw∈RnD×nD
    expresses the conservative power exchanges between dissipative components;
Jy∈RnP×nP
    expresses the conservative power exchanges between ports (direct connections of inputs to outputs);
K∈RnS×nD
    expresses the conservative power exchanges between the storage components and the dissipative components;
Gx∈RnS×nP
    expresses the conservative power exchanges between ports and storage components (input gain matrix);
Gw∈RnD×nP

    expresses the conservative power exchanges between ports and dissipative components (input gain matrix).

The PHS (5) fulfills the definition of passivity (e.g., [16]) according to the following property.
Property 1 (Power Balance). The variation of the total energy E=H(x)
of a system governed by (5) is given by (1), with D=z(w)⊺⋅w≥0 the total dissipated power, and S=u⊺⋅y
the total power incoming on external ports.
Proof.  We have a⊺⋅b=dEdt+D−S
. Now a⊺⋅b=a⊺⋅J⋅a=0 since J
is skew-symmetric. ☐
Remark 1 (Power variables). This work is devoted to the treatment of electronic circuits for which power variables are chosen as current and voltage. However, all the aforementioned definitions apply equally to multiphysical systems, provided an adapted set of power variables, generically denoted by flux (currents, velocities, magnetic flux variations) and efforts (voltages, forces, magnetomotive force), the product of which is a power (see [23] Table 1.1). This follows the bond-graph modeling approach [28,29], on which the PHS formalism is built (see [23] §1.6 and 2.1). The treatment of multiphysical audio systems in the PHS formalism can be found in [30] (electromechanical piano that includes mechanical, electrical, and magnetic phenomena) and [31] (§III.B) (modulated air flow for musical acoustics applications that includes mechanical and acoustical phenomena).

## 1.2. Example
Consider the resistor-inductor-capacitor (RLC) circuit in Figure 1, with nS=2
, nD=1, and nP=2, described as follows. For the linear inductance L, the state and the positive definite function can be the magnetic flux x1=ϕ and h1(ϕ)=ϕ2/(2L), so that vL=dh1/dx1 and iL=dx1dt. For the capacitance and the resitance, quantities are defined with x2=q and w=[iR]. Port variables are arranged as input u=[v1,v2]⊺ and output y=[−i1,−i2]⊺
(edges receiver convention).
Applsci 06 00273 g001 550
Figure 1. Resistor-inductor-capacitor (RLC) circuit (notations and orientations).
Applying Kirchhoff’s laws to this simple serial circuit yields
⎛⎝⎜⎜⎜⎜⎜⎜⎜vLiCiRi1i2⎞⎠⎟⎟⎟⎟⎟⎟⎟=⎛⎝⎜⎜⎜⎜⎜⎜⎜0+1+1+1−1−10000−10000−10000+10000⎞⎠⎟⎟⎟⎟⎟⎟⎟⋅⎛⎝⎜⎜⎜⎜⎜⎜⎜iLvCvRv1v2⎞⎠⎟⎟⎟⎟⎟⎟⎟.
From the constitutive laws of components, this equation restores the form (5) exactly, block by block. It provides the algebraic-differential equations that govern the system with input u
and output y
.
This work aims at simulating such passive systems by firstly generating Equation (5) associated to a given circuit, and secondly by deriving its numerical version so that a discrete power balance is satisfied.
Remark 2 (Reduction). The system (5) can be reduced by decomposing function z
into its linear and nonlinear parts. See Appendix A for details.

References
-----------

.. [FH2016] Falaize, A., & Hélie, T. (2016). Passive Guaranteed Simulation of Analog Audio Circuits: A Port-Hamiltonian Approach. Applied Sciences, 6(10), 273.
