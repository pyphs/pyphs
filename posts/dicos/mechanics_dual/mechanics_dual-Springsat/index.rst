
.. title: Saturating spring (Springsat)
.. slug: mechanics_dual-Springsat
.. date: 2019-04-28 12:31:26.766724
.. tags: mechanics_dual, mathjax
.. category: component
.. type: text

Saturating spring from [1]_ (chap 7) with state :math:`q\in [-q_{sat}, q_{sat}]` and parameters described below. The energy is

.. math::

    H(q) = K_0 \, \left( \frac{q^2}{2} +  K_{sat} H_{sat}(q)\right),

with

.. math::

    H_{sat}(q) = -  \frac{8 q_{sat}}{\pi \left(4-\pi\right)} \, \left(\frac{\pi^{2} q^{2}}{8q_{sat}^{2}} + \log{\left (\cos{\left (\frac{\pi q}{2 q_{sat}} \right)} \right)}\right).

The resulting force is:

.. math::

    f(q)= \frac{d\,H(q)}{d q} = K_{0} \left(q + K_{sat} \frac{d\,H_{sat}(q)}{d q}\right),

with

.. math::

    \frac{d\,H_{sat}(q)}{d q}= \frac{4}{4- \pi} \left(\tan{\left (\frac{\pi q}{2 q_{sat}} \right )} - \frac{\pi q}{2q_{sat}} \right).



.. TEASER_END

None
