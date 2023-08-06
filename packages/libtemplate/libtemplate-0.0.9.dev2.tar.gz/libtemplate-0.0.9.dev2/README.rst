========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/libtemplate/badge/?style=flat
    :target: https://libtemplate.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/jpardovega/libtemplate.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/jpardovega/libtemplate

.. .. |requires| image:: https://requires.io/github/jpardovega/libtemplate/requirements.svg?branch=master
..     :alt: Requirements Status
..     :target: https://requires.io/github/jpardovega/libtemplate/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/jpardovega/libtemplate/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/jpardovega/libtemplate

.. |version| image:: https://img.shields.io/pypi/v/libtemplate.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/libtemplate

.. |wheel| image:: https://img.shields.io/pypi/wheel/libtemplate.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/libtemplate

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/libtemplate.svg
    :alt: Supported versions
    :target: https://pypi.org/project/libtemplate

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/libtemplate.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/libtemplate

.. |commits-since| image:: https://img.shields.io/github/commits-since/jpardovega/libtemplate/v0.0.8.svg
    :alt: Commits since latest release
    :target: https://github.com/jpardovega/libtemplate/compare/v0.0.1...master



.. end-badges

Template for python packages generated with cookiecutter-pylibrary

Installation
============

::

    pip install libtemplate

You can also install the in-development version with::

    pip install https://github.com/jpardovega/libtemplate/archive/master.zip


Documentation
=============


https://libtemplate.readthedocs.io/


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
