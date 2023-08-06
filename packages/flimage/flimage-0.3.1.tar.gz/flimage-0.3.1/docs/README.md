flimage documentation
=====================
To install the requirements for building the documentation, run

    pip install -r requirements.txt

To compile the documentation, run

    sphinx-build . _build


Notes
=====
To view the sphinx inventory of flimage, run

   python -m sphinx.ext.intersphinx 'http://flimage.readthedocs.io/en/latest/objects.inv'
