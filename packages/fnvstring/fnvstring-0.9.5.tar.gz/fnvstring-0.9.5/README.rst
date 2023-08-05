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
   my_hasher = Fvn64SaltedHasher(salt='Any$tringYouWant, even none')
   print(my_hasher.hash('Hello World!')) # Must output dcSEMoww20o if you dont chant the salt param

