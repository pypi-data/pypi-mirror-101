==================
Character Encoding
==================

Commodore systems used a 7-bit character encoding commonly referred to
as PETSCII. Modern computer systems use a variable length encoding
called Unicode. In order to translate between these formats a set of
encoding and decoding tables known as codecs are used.

Multiple codecs exist because there are multiple variants of PETSCII
which differ slightly between different models. In addition most
systems have two separate character sets

#. upper case letters and graphics characters
#. lower case and upper case letters

When displaying the contents of directories and BASIC strings the
current codec is used to produce the correct representation. It is
also used for converting file names entered by the user.

The current codec is stored in the ``encoding`` setting:

.. code-block:: text

    (cbm) set encoding
    encoding: 'petscii-c64en-uc'

The middle part is a combination of the system name followed by the
language. The final part of the encoding name indicates the case, to
switch to a codec with lower case characters set a new value ending
``lc``:

.. code-block:: text

    (cbm) set encoding petscii-c64en-lc
    encoding - was: 'petscii-c64en-uc'
    now: 'petscii-c64en-lc'

Control Characters
------------------

PETSCII contains many non-printing control characters which cause
effects such as a change of foreground colour, reverse video
etc. These are usually displayed as a reverse video character, for
example a reverse video ``S`` represents the cursor home character.

These representations are not easy to enter in Unicode and are
therefore replaced by a string enclosed in curly brackets, for example
the cursor home character is shown as ``{home}``.

The mapping of these sequences is achieved by a separate table derived
from the current codec.
