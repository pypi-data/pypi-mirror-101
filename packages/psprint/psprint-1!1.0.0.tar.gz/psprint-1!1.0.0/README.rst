#########
PSPRINT
#########

*********
Gist
*********

Source Code Repository
=======================

|source| `Repository <https://github.com/pradyparanjpe/psprint.git>`__


Badges
======

|Documentation Status|  |PyPi Version|  |PyPi Format|  |PyPi Pyversion|


************
Description
************

Prompt-String-like Print.

[ INFO ]Print statements with a flexible descriptor prefix for better
readability.

What does it do
===============

::

   #!/usr/bin/env python3
   # -*- coding: utf-8; mode: python; -*-

   print()
   print("*** WITHOUT PSPRINT ***")
   print("An output statement which informs the user")
   print("This statement requests the user to act")
   print("A debugging output useless to the user")
   print()

   from psprint import print
   print()
   print("*** WITH PSPRINT ***")
   print("An output statement which informs the user", mark=1)
   print("This statement requests the user to act", mark=2)
   print("A debugging output useless to the user", mark='bug')
   print ()

Screenshot:

.. figure:: docs/output.jpg
   :alt: screenshot

   screenshot

.. |Documentation Status| image:: https://readthedocs.org/projects/psprint/badge/?version=latest
   :target: https://psprint.readthedocs.io/?badge=latest
.. |source| image:: https://github.githubassets.com/favicons/favicon.png
   :target: https://github.com/pradyparanjpe/psprint.git

.. |PyPi Version| image:: https://img.shields.io/pypi/v/psprint
   :target: https://pypi.org/project/psprint/
   :alt: PyPI - version

.. |PyPi Format| image:: https://img.shields.io/pypi/format/psprint
   :target: https://pypi.org/project/psprint/
   :alt: PyPI - format

.. |PyPi Pyversion| image:: https://img.shields.io/pypi/pyversions/psprint
   :target: https://pypi.org/project/psprint/
   :alt: PyPi - pyversion
