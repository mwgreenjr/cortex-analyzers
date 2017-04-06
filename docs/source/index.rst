.. TheHive Analyzer for JAMIE documentation master file, created by
   sphinx-quickstart on Thu Mar  9 14:53:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CERT-Bund TheHive/Cortex Analyzer Subset
========================================
Build
-----

.. image:: https://travis-ci.org/BSI-CERT-Bund/cortex-analyzers.svg?branch=master
    :target: https://travis-ci.org/BSI-CERT-Bund/cortex-analyzers

About
-----
TheHive is a security incident response software, which is segmented in ui and backend
(`TheHive <https://github.com/CERT-BDF/TheHive>`_) as well as the analyzer backend
(`Cortex <https://github.com/CERT-BDF/Cortex-Analyzers/>`_). This repository contains our set of analyzers we're using
for JAMIE (**J**\ oint **A**\ nalysis for **M**\ alware and **I**\ ncident **E**\ valuation). All necessary information
about installation and configuration regarding the modules can be found in this documentation.

Dependency installation
-----------------------
Because the python ``typing`` `library <https://docs.python.org/3/library/typing.html>`_ is used, python v. >=3.5 is
needed to run this analyzers. If you need to install multiple python versions, you can take a look at the
``make altinstall`` part in the `python documentation <https://docs.python.org/3.6/using/unix.html#building-python>`_.

When using multiple python versions, you may change the shebang (#!) part in the analyzer python files to
``#!/usr/bin/env python3.5`` or something like that.

.. code-block:: bash

   # Build cortexutils3
   python3 setup.py build

   # Install cortexutils3
   sudo python3 setup.py install

   # Install analyzers dependencies
   # (and sphinx for building the documentation)
   sudo pip3 install -r requirements.txt

Installing cortex-analyzers
---------------------------
Take a look into the official documentation available in the CERT-BDF/Cortex
`github wiki <https://github.com/CERT-BDF/Cortex/wiki/Analyzers>`_ (especially the ``path`` parameter).

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Table of contents

   example
   cortexutils3
   certatpdns
   circlpdns
   circlpssl
   firehol
   misp
   safebrowsing
   virusshare
   vmray
   yara


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
