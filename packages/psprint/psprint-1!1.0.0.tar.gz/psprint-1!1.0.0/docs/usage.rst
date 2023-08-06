#####
USAGE
#####

Substitute python's print
=========================

Import in your script.

.. code:: python

          from psprint import print

Supply value for ``mark`` kwarg or for any of the custom kwargs as described.

.. code:: python

          print("", mark="info")


.. note::

    You may have to add exception to ``${XDG_CONFIG_HOME}/pylintrc`` if you use linter

.. code:: ini

    [VARIABLES]
    redefining-builtins-modules=psprint


Configure frequently used ``mark`` in a suitably `located <configure.html#location-of-configuration-files>`__ configuration file.


