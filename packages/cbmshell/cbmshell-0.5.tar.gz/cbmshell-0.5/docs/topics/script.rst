=============
Using Scripts
=============

As well as using ``cbm-shell`` interactively pre-created scripts can
be executed from the command line.

Commands must be stored in a text file, one command per line. The
script is then invoked using the ``@`` shortcut:

.. code-block:: shell

    $ cbm-shell @scriptfile

Scripts should end with ``quit`` as the final command, otherwise
``cbm-shell`` prompts for further commands.
