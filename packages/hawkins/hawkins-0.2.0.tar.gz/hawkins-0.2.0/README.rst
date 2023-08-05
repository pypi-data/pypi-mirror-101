========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|


.. |version| image:: https://img.shields.io/pypi/v/hawkins.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/hawkins

.. |wheel| image:: https://img.shields.io/pypi/wheel/hawkins.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/hawkins

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/hawkins.svg
    :alt: Supported versions
    :target: https://pypi.org/project/hawkins

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/hawkins.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/hawkins

.. |commits-since| image:: https://img.shields.io/github/commits-since/miguelcfsilva11/Hawkins_Chess-AI/v1.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/miguelcfsilva11/Hawkins_Chess-AI/compare/v1.0.0...master



.. end-badges

"Hawkins" is an open-source, competitive Chess AI powered by multiple tree search algorithms. It makes use of various
optimization techniques, mostly extensions of alpha-beta pruning and other traditional chess engine methods. It comes
with its own GUI and many levels of difficulty.

* Free software: MIT license

Installation
============

::

    pip install hawkins

You can also install the in-development version with::

    pip install https://github.com/miguelcfsilva11/Hawkins_Chess-AI/archive/master.zip


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
