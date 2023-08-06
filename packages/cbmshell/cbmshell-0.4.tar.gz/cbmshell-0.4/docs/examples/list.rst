===========================
Working with BASIC Programs
===========================

Making Changes
--------------

``cbm-shell`` can be used to quickly edit BASIC programs without
starting up an emulator:

.. code-block:: text

    (cbm) list 0:MYPROGRAM myprogram.txt
    (cbm) edit myprogram.txt
    [perform changes, save and exit editor]
    (cbm) unlist myprogram.txt 0:NEWPROGRAM
 
Different variants of BASIC
---------------------------

Change the current token set before using ``list`` or ``unlist``:

.. code-block:: text

    (cbm) set token_set basic-v4
    token_set - was: 'basic-v2'
    now: 'basic-v4'
    (cbm) list 0:BASIC4TEST
    10 REM BASIC 4
    20 SCRATCH"THING" ON U9
