fnvstring
=========

**fnvstring** is a hash implementation of the Fowler–Noll–Vo non-cryptographic
function.

Installation
^^^^^^^^^^^^

.. code:: shell

   $ pip install fnvstring

.

Usage
~~~~~

usage in terminal
-----------------

You can hash any string from terminal just typing

.. code:: shell

   $ fnvstring "Hello World!"
   rzWLzszm9JE

usage in code
-------------

.. code:: python

   from fnvstring import Fvn64SaltedHasher
   my_hasher = Fnv64SaltedHasher(salt='Any$tringYouWant, even none')
   print(my_hasher.hash('Hello World!')) # Will output 63COXAuMHMw if you don't change this salt param
