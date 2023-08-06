=============
Copying Files
=============

Files can be moved between images or between an image and the local
filesystem using the ``copy`` command:

.. code-block:: text

    (cbm) copy 0:MYFILE myfile.prg
    Copying ImagePath(0:b'MYFILE') to myfile.prg

Multiple source files, or even entire drives, may be given as long as
the destination (the final argument) is either a drive or a directory:

.. code-block:: text

    (cbm) copy 0:FILE1 1:FILE2 backup/
    Copying ImagePath(0:b'FILE1') to backup/FILE1
    Copying ImagePath(1:b'FILE2') to backup/FILE2

When copying from the local filesystem to an image the file type must
be supplied:

.. code-block:: text

    (cbm) copy --type PRG myfile.prg 0:MYFILE
    Copying myfile.prg to ImagePath(0:b'MYFILE')
