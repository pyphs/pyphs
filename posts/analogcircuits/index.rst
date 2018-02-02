.. title: Analog audio circuits
.. slug: analogcircuits
.. date: 2016-06-21 01:06:53 UTC+02:00
.. tags: mathjax
.. category: effect
.. link:
.. description:
.. type: text
.. author: Antoine Falaize

This is a companion page for the article **Passive guaranteed simulation of analog audio circuits: A port-Hamiltonian approach**
submitted in may 2016 to the special issue *Audio Signal Processing* of journal `Applied Science <http://www.mdpi.com/journal/applsci>`_.

.. TEASER_END: click to acces simulated sounds

Comparison of numerical methods
--------------------------------

A detailed comparison with simulation code are available `here </posts/comparisonnumschemes/>`_.

Diode clipper
--------------

+----------------------------------------------------------------------+------------------------------------------------------------------+
|    .. figure:: /images/analogcircuits/Diode_clipper_schematic.png    |    .. figure:: /images/analogcircuits/Diode_clipper_signal.png   |
|        :width: 150px                                                 |        :width: 400px                                             |
|        :scale: 100 %                                                 |        :scale: 100 %                                             |
|        :align: center                                                |        :align: center                                            |
+----------------------------------------------------------------------+------------------------------------------------------------------+

BJT audio amplifer
--------------------

+----------------------------------------------------------------------+------------------------------------------------------------------+
|    .. figure:: /images/analogcircuits/BJT_amp_schematic.png          |    .. figure:: /images/analogcircuits/BJT_amp_signal.png         |
|        :width: 200px                                                 |        :width: 400px                                             |
|        :scale: 100 %                                                 |        :scale: 100 %                                             |
|        :align: center                                                |        :align: center                                            |
+----------------------------------------------------------------------+------------------------------------------------------------------+
|    .. figure:: /images/analogcircuits/bjt_PHS.png                    |    .. figure:: /images/analogcircuits/bjt_LTspice.png            |
|        :width: 500px                                                 |        :width: 400px                                             |
|        :scale: 100 %                                                 |        :scale: 100 %                                             |
|        :align: center                                                |        :align: center                                            |
+----------------------------------------------------------------------+------------------------------------------------------------------+

CryBaby wah pedal
------------------

Original

	Short guitar sample

	.. raw:: html

		<audio controls>
			<source src="/sounds/analogcircuits/Chunky_Riff.mp3">
		</audio>

CryBaby output

	The *wah* parameter (potentiometer coefficient) is continuously varying according to a sinusoid signal with DC offset 0.5, amplitude 1 and frequency 1Hz.

	.. raw:: html

		<audio controls>
			<source src="/sounds/analogcircuits/PHS_wah.mp3">
		</audio>
