.. turn this document into an HTML page by typing `scons`

About
-----

This is a collection of `SCons`_ tools for automating the Xilinx build flow.

.. _SCons: http://www.scons.org/

:Author:  Michael Krieger, SuS
:Contact: michael.krieger@ziti.uni-heidelberg.de
:Date:    2014-03

- Contents: *to do*
- Usage: *to do*
- Example project: *to do*

Installation
------------

Copy the entire ``xilinx`` directory into a directory
``<scons-root>/site_scons/site_tools``, where ``<scons-root>`` must be
visible to SCons when invoked.

By default, SCons accepts the following locations as ``<scons-root>``:

- the current working directory
- ``~/.scons`` (single-user only)
- ``/usr/share/scons`` (system wide)

The file copying is handled for you if you call

::

    scons install [--user]

where the presence of the ``--user`` option selects between the
``~/.scons`` and the ``/usr/share/scons`` location.
