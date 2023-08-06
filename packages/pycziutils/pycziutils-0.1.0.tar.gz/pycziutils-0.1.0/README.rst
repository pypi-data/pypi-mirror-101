==========
pycziutils
==========


.. image:: https://img.shields.io/pypi/v/pycziutils.svg
        :target: https://pypi.python.org/pypi/pycziutils

.. image:: https://img.shields.io/travis/yfukai/pycziutils.svg
        :target: https://travis-ci.org/yfukai/pycziutils

.. image:: https://ci.appveyor.com/api/projects/status/yfukai/branch/master?svg=true
    :target: https://ci.appveyor.com/project/yfukai/pycziutils/branch/master
    :alt: Build status on Appveyor

.. image:: https://readthedocs.org/projects/pycziutils/badge/?version=latest
        :target: https://pycziutils.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Python utilities to read (tiled) CZI files and parse metadata through python-bioformats


* Free software: BSD license

* Documentation: https://pycziutils.readthedocs.io.


Installation:
-------------

.. code-block:: console

    $ pip install pycziutils

Features
--------

A tiny utility module to parse Zeiss CZI files in Python through python-bioformats.
Parse tiled images, organize planes into pandas.DataFrame, parse some hard-to-get metadata.

Example
-------

.. code-block:: python
    
    import pycziutils
   
    @with_javabridge
    def main():
        tiled_czi_ome_xml=pycziutils.get_tiled_omexml_metadata("path/to/czi/file.czi")
        tiled_properties_dataframe=pycziutils.parse_planes(tiled_czi_ome_xml)
        print(tiled_properties_dataframe.columns)
        #
        print(tiled_properties_dataframe.iloc[0])
        #

        reader=pycziutils.get_tiled_czi_reader("path/to/czi/file.czi") #returns bioformats reader for tiled images
        for i, row in tiled_properties_dataframe.iterrows():
            image=reader.read(s=row["image"],t=row["T_index"],z=row["Z_index"],c=row["C_index"])
        
        bit_depth=pycziutils.get_camera_bits(tiled_czi_ome_xml)
        # do whatever you like to do with javabridge, with adjusted log level!

    if __name__=="__main__":
        main()

TODO
----
- Generate documentation
- Writing tests and Github actions

Credits
-------

This package was created with Cookiecutter_ and the `wboxx1/cookiecutter-pypackage-poetry`_ project template.

This package is using pysen_ for linting and formatting. 

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`wboxx1/cookiecutter-pypackage-poetry`: https://github.com/wboxx1/cookiecutter-pypackage-poetry
.. _pysen: https://github.com/pfnet/pysen
