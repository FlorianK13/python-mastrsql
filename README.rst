.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/mastrsql.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/mastrsql
    .. image:: https://readthedocs.org/projects/mastrsql/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://mastrsql.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/mastrsql/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/mastrsql
    .. image:: https://img.shields.io/pypi/v/mastrsql.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/mastrsql/
    .. image:: https://img.shields.io/conda/vn/conda-forge/mastrsql.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/mastrsql
    .. image:: https://pepy.tech/badge/mastrsql/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/mastrsql


.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

===============
mastrsql
===============


    A python package to download the german Marktstammdatenregister (short: MaStR) and save it as a local PostgreSQL database.


The german *Federal Network Agency for Electricity, Gas, Telecommunications, 
Post and Railway* (Bundesnetzagentur) publishes their data set of all electricity and gas producers openly 
on their website_. This data set is called *Markstammdatenregister* (short: MaStR). As a relatively new feature (as of 2021), 
they offer a complete `data download`_ in zipped xml format 
besides their API_. The scope of the mastrsql package is to offer an easy and automated download of the MaStR into a local 
PostgreSQL database. It is planned to expand the package to also include an update function, that only downloads new entries
which are not yet saved in the local database via the API. If you're looking for other features, also check out `open-Mastr`_

Quick Start
============
Install PostgreSQL_, either on your own or with the help of a tutorial video_ (for Linux).
Install the package from PyPI (as soon as it is published there).

.. code:: bash

    pip install mastrsql


Import the Mastr class and define a Mastr object.

>>> from mastrsql.mastr import Mastr 

The *postgres_standard_credentials* depend on your postgres configuration. Check the given credentials before using them, 
otherwise an error will occure.

>>> postgres_standard_credentials = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        }

>>> database = Mastr(postgres_standard_credentials=postgres_standard_credentials)

Download the latest version of the zipped MaStR in xml format.

>>> database.download()

Read the downloaded files into a PostgreSQL database.

>>> database.to_sql()

For extracting information from the local PostgreSQL database we refer to other packages, for example you can use `pandas.read_sql`_.

Note
====

This project has been set up using PyScaffold 4.1.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.


.. _website: https://www.marktstammdatenregister.de/MaStR
.. _data download: https://www.marktstammdatenregister.de/MaStR/Datendownload 
.. _API: https://www.marktstammdatenregister.de/MaStRHilfe/subpages/webdienst.html
.. _pandas.read_sql: https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html
.. _open-Mastr: https://open-mastr.readthedocs.io/en/dev/
.. _PostgreSQL: https://www.postgresql.org/
.. _video: https://www.youtube.com/watch?v=-LwI4HMR_Eg


