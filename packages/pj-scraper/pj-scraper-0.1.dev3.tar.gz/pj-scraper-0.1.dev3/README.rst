========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis|
        |
        | |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |travis| image:: https://api.travis-ci.com/mdhor/pj-scraper.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/mdhor/pj-scraper

.. |codeclimate| image:: https://codeclimate.com/github/mdhor/pj-scraper/badges/gpa.svg
   :target: https://codeclimate.com/github/mdhor/pj-scraper
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/pj-scraper.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pj-scraper

.. |wheel| image:: https://img.shields.io/pypi/wheel/pj-scraper.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pj-scraper

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pj-scraper.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pj-scraper

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pj-scraper.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pj-scraper

.. |commits-since| image:: https://img.shields.io/github/commits-since/mdhor/pj-scraper/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/mdhor/pj-scraper/compare/v0.0.0...master



.. end-badges

none

* Free software: MIT license

Installation
============

::

    pip install pj-scraper

You can also install the in-development version with::

    pip install https://github.com/mdhor/pj-scraper/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    import pj_scraper
    pj_scraper.longest()


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
