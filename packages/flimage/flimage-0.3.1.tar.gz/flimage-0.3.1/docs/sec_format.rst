================
HDF5 file format
================

The data of a :class:`flimage.FLImage` or :class:`flimage.FLSeries` can be
stored on disk, using the ``h5file`` parameter upon class instantiation.
This section describes the scheme used to store the data using the
`HDF5 file format <https://en.wikipedia.org/wiki/Hierarchical_Data_Format#HDF5>`_.

FLImage
=======
The following graph visualized the HDF5 file structure of an FLImage instance:

.. graphviz::

     graph example {
         graph [rankdir=LR];
         FLImage [shape="folder", label="/"];
         fluorescence [shape="folder"];
         raw [shape="component"];
         bg_data [shape="folder"];
         data [shape="component"];
         FLImage -- fluorescence;
         fluorescence -- raw;
         fluorescence -- bg_data;
         bg_data -- data;
     }


Attributes
----------
These attributes of the root group (/) describe physical parameters of the data:

.. flimage_meta_table:: data


These other attributes may be used by e.g. data simulators such as
:ref:`cellsino <cellsino:index>`:

.. flimage_meta_table:: other


Groups
------
The group *fluorescence* does not hold attributes. It contains
a dataset called *raw* (the raw fluorescence image) and a group called
*bg_data* which may contain a dataset *data*,
a simple background image.


FLSeries
========
The following graph visualized the HDF5 file structure of an FLSeries instance
(with a total of 48 FLImages):

.. graphviz::

     graph example {
         node [shape="folder"];
         graph [rankdir=LR, center=1];
         FLSeries [label="/"]
         fl1 [label="fli_0"]
         fl2 [label="fli_1"]
         a1 [shape="box", label=fluorescence];
         d0 [shape="box", label="..."];
         d2 [shape="box", label="..."];
         d3 [shape="box", label="..."];
         d4 [shape="box", label="..."];
         fl3 [label="fli_47"]
         FLSeries -- fl1;
         fl1 -- a1;
         a1 -- d0;
         FLSeries -- fl2;
         fl2 -- d2;
         FLSeries -- d4;
         FLSeries -- fl3;
         fl3 -- d3;
     }

Note that the name of each FLImage group always starts with "fli\_" and that the
enumeration does not contain leading zeros. The root node (/) of an FLSeries
may have the *identifier* attribute.
