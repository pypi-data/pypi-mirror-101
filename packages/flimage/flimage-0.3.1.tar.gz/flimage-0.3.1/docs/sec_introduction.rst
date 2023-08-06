============
Introduction
============

.. toctree::
  :maxdepth: 2


The Problem
===========
In correlative fluorescence and refractive index tomography, it is sometimes
necessary to record phase and fluorescence images with different cameras,
different frame rates, and different resolutions :cite:`Schuermann2017`.
Handling these images and frame times easily gets out of hand
(especially when they are stored in different files) and it would be nice
to have a unified, data-driven interface to single fluorescence images
and fluorescence series.


Why flimage?
============
There already exist many file formats for fluorescence data. I know that.
However, I have made good experiences with the :ref:`qpimage <qpimage:index>`
file format approach and wanted to have a similar API for the fluorescence
data. This makes it easier to write transparent code for tomographic image
analysis. Flimage also comes with a convenient bleach correction function.


Citing flimage
==============
If you are using flimage in a scientific publication, please
cite it with:

::

  (...) using flimage version X.X.X (available at
  https://pypi.python.org/pypi/flimage).

or in a bibliography

::
  
  Paul Müller (2017), flimage version X.X.X: Phase image analysis
  [Software]. Available at https://pypi.python.org/pypi/flimage.

and replace ``X.X.X`` with the version of flimage that you used.
