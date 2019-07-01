
.. title: Cubic spring (Springcubic)
.. slug: mechanics_dual-Springcubic
.. date: 2019-04-28 12:31:26.766431
.. tags: mechanics_dual, mathjax
.. category: component
.. type: text

Cubic spring with state :math:`q\in \mathbb R` and parameters described below. The energy is

.. math::

    H(q) = \frac{F_1\,q^2}{2\,q_{ref}} + \frac{F_3\,q^4}{4q_{ref}^3}.

The resulting force is:

.. math::

    f(q)= \frac{d \, H(q)}{d q} = F_1 \,\frac{q}{q_{ref}} + F_3 \, \frac{q^3}{q_{ref}^3}.

so that :math:`f(q_{ref}) = F1+F3`.

.. TEASER_END

None
