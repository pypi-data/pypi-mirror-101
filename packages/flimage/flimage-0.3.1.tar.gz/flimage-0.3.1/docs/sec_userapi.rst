========
User API
========
The flimage API is built upon the hdf5 file format using
`h5py <http://h5py.readthedocs.io/>`_. It is almost identical to the
:ref:`user API of qpimage <qpimage:userapi>`.
Each instance of :py:class:`flimage.FLImage <flimage.core.FLImage>`
generates an hdf5 file, either on disk or in memory, depending on the
preferences of the user.


Storing FLImage data on disk
----------------------------
To cache the FLImage data on disk, use the ``with``
statement in combination with the ``h5file`` keyword argument

.. code-block:: python

   with flimage.FLImage(data=fluorescence_ndarray, h5file="/path/to/file.h5"):
       pass

where all data is stored in ``/path/to/file.h5``. This will create an hdf5
file on disk that, at a later time point, can be used to create an instance
of `FLImage`:

.. code-block:: python

   # open previously cached data for reading
   fli = flimage.FLImage(h5file="/path/to/file.h5", h5mode="r")
   
   # or open cached data for writing (e.g. for changing the background)
   with flimage.FLImage(h5file="/path/to/file.h5", h5mode="a") as fli:
       # do something here

The default value of ``h5mode`` is "a", which means that data
will be overridden. In the hdf5 file, the following data is stored:

- all data for reproducing the background-corrected fluorescence
  (``fli.fluorescence``) including
  
  - the experimental fluorescence data
  - the experimental background data

- all measurement specific meta data, given by the keyword argument
  ``meta_data``

Dealing with measurement series
-------------------------------
Flimage also comes with a :py:class:`FLSeries <flimage.series.FLSeries>`
class for handling multiple instances of FLImage in one hdf5 file. 
For instance, to combine two FLImages in one series file, one could
use:

.. code-block:: python

   paths = ["file_a.h5", "file_b.h5", "file_c.h5"]

   with flimage.FLSeries(h5file="/path/to/series_file.h5", h5mode="w") as fls:
       for ii, pp in enumerate(paths):
           fli = flimage.FLImage(h5file="/path/to/file.h5", h5mode="r")
           fls.add_flimage(fli=fli, identifier="my_name_{}".format(ii))

Note that the function `add_flimage` accepts the optional keyword argument
"identifier" (overriding the identifier of the FLImage) which
can also be used for indexing later:

.. code-block:: python

   with flimage.FLSeries(h5file="/path/to/series_file.h5", h5mode="r") as fls:
       # these two are equivalent
       fli = fls[0]
       fli = fls["my_name_0"]


Notes
-----
- Even though the hdf5 data is stored as gzip-compressed single precision
  floating point values, using flimage hdf5 files
  may result in file sizes that are considerably
  larger compared to when only the output of e.g. ``qpi.fluorescence`` is stored
  using e.g. :py:func:`numpy.save`.

- Units in flimage follow the international system of units (SI).

- :py:class:`flimage.FLSeries <flimage.series.FLSeries>` provides convenience
  functions for bleach correction.
