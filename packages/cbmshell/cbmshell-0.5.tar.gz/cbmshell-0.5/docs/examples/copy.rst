=============
Copying Files
=============

Copying a file from an image to the local filesystem:

.. code-block:: text

    (cbm) copy 0:MYFILE myfile.prg
    Copying ImagePath(0:b'MYFILE') to myfile.prg

Copying all files in an image to a local directory:

.. code-block:: text

    (cbm) copy 0: folder/
    Copying ImagePath(0:b'FILE1') to folder/FILE1
    Copying ImagePath(0:b'FILE2') to folder/FILE2
    Copying ImagePath(0:b'FILE3') to folder/FILE3

Copying all sequential data files from two images to a third image:

.. code-block:: text

    (cbm) copy 0:*=S 1:*=S 2:
    Copying ImagePath(0:b'DATA1') to ImagePath(2:b'DATA1')
    Copying ImagePath(0:b'DATA2') to ImagePath(2:b'DATA2')
    Copying ImagePath(1:b'DATA8') to ImagePath(2:b'DATA8')

Copying a BASIC program file from the local filesystem to an image:

.. code-block:: text

    (cbm) copy --type PRG myfile.prg 0:MYFILE
    Copying myfile.prg to ImagePath(0:b'MYFILE')
