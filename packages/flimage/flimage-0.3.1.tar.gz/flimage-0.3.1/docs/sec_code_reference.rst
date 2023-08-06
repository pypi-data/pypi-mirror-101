==============
Code reference
==============
This section does not cover the base classes, methods, and constants of
:ref:`qpimage <qpimage:index>`, which can be found
:ref:`here <qpimage:coderef>`.


.. toctree::
  :maxdepth: 2


module level aliases
====================
For user convenience, the following objects are available
at the module level.

.. class:: flimage.FLImage
    
    alias of :class:`flimage.core.FLImage`

.. class:: flimage.FLSeries
    
    alias of :class:`flimage.series.FLSeries`

.. data:: flimage.META_KEYS_FL

    alias of :data:`flimage.meta.META_KEYS_FL`  


.. _core:

core (FLImage)
==============

Classes
-------
.. autoclass:: flimage.core.FLImage
   :members:
   :undoc-members:



.. _image_data:

image_data (basic image management)
===================================

Classes
-------
.. automodule:: flimage.image_data
   :members: Fluorescence
   :undoc-members:
   :show-inheritance:


.. _meta:

meta (definitions for FLImage meta data)
========================================

Constants
---------
.. autodata:: flimage.meta.META_KEYS_FL


.. _series:

series (FLSeries)
=================

Classes
-------
.. autoclass:: flimage.series.FLSeries
   :members:
   :undoc-members:
