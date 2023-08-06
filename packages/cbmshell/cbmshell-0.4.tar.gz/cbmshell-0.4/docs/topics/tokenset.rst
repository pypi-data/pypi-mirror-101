================
BASIC Token Sets
================

Files that contain BASIC programs encode keywords such as PRINT as
8-bit values called tokens. To expand a program file to text a mapping
of token to string is needed, a similar mapping (in reverse) is used
to convert text file to a program file.

Different Commodore systems had different versions of BASIC and
therefore multiple token sets are needed. In addition various ROM
cartridges and other extensions have their own token sets.

The list of available token sets can be printed:

.. code-block:: text

    (cbm) token_set
    basic-v2
    basic-v4
    vic20-super-expander
    vic20-super-expander-jp

The current token set is stored in the ``token_set`` setting:

.. code-block:: text

    (cbm) set token_set
    token_set: basic-v2

To change the current token set assign a new value:

.. code-block:: text

    (cbm) set token_set vic20-super-expander
    token_set - was: 'basic-v2'
    now: 'vic20-super-expander'
