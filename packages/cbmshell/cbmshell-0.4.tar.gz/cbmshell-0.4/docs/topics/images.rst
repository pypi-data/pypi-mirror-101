Managing Images
===============

For ``cbm-shell`` to be able to access the contents of an image it
must be associated with a drive number. That is done by attaching the
image:

.. code-block:: text

    (cbm) attach mydisk.d64 
    Attached mydisk.d64 to 0

Up to ten images may be attached at any one time.

To prevent modifications to an image it may be attached read-only

.. code-block:: text

    (cbm) attach --read-only mydisk.d64 

When an image is no longer required it may be detached:

.. code-block:: text

    (cbm) detach 0
    Detached D64Image(mydisk.d64)

The list of currently attached images can be displayed using the
``images`` command:

.. code-block:: text

    (cbm) images
        0  RW  D64Image(mydisk.d64)
