Listing Directories
===================

The contents of an image can be displayed using the ``directory``
command:

.. code-block:: text

    (cbm) directory
    0 "DIGITALMONASTERY"  2 1A
    67   "ZOMBIE C.P.  /DM" PRG
    17   "ZOMBIE DOCS  /DM" PRG
    0    "────────────────" DEL
    0    " VIC20 32K PAL  " DEL
    0    "    REQUIRED    " DEL
    0    "────────────────" DEL
    580 BLOCKS FREE.

By default the directory of all images is printed, one or more drive
numbers can be given as arguments.

DOS wildcards may be used to list only those files that match a
pattern:

.. code-block:: text

    (cbm) directory 0:*=P
    0 "DIGITALMONASTERY"  2 1A
    67   "ZOMBIE C.P.  /DM" PRG
    17   "ZOMBIE DOCS  /DM" PRG
    580 BLOCKS FREE.

The shortcut ``$`` may also be used instead of ``directory``.
