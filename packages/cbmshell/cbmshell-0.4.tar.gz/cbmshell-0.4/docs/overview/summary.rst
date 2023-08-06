.. _pypi: https://pypi.org/

Install the Python ``cbmshell`` package from pypi_ using:

.. code-block:: shell

    $ pip install cbmshell

Start an interactive session by running:

.. code-block:: shell

    $ cbm-shell
    (cbm)

Commands entered following the ``(cbm)`` prompt will be immediately
executed. To see a list of supported commands use ``help``:

.. code-block:: text

    (cbm) help
  
    Documented commands (use 'help -v' for verbose/'help <topic>' for details):
    ===========================================================================
    alias   delete     edit  history  macro  run_pyscript  shell      unlist
    attach  detach     file  images   py     run_script    shortcuts
    copy    directory  help  list     quit   set           token_set

Disk images are made available by attaching them to a drive number:

.. code-block:: text

    (cbm) attach mydisk.d64 
    Attached mydisk.d64 to 0

Many commands can work with either a file on the local filesystem:

.. code-block:: text

    (cbm) list test.prg

or a file inside an image:

.. code-block:: text

    (cbm) list 0:PRINT

or a combination of both:

.. code-block:: text

    (cbm) copy 0:TEST test.prg
