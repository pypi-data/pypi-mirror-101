thorlabs_mc2000b
================

This is an interface to the Thorlabs MC2000B optical chopper unit, communicating over the USB
serial port.

Information about the unit can be found on the `product webpage <https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=287>`_,
and details of the commands and how they apply to the different models of chopper blades can be
found in the `user manual <https://www.thorlabs.com/_sd.cfm?fileName=TTN102010-D02.pdf&partNumber=MC2000B-EC>`_.

Usage is quite straightforward. For example:

.. code-block:: python

    from thorlabs_mc2000b import MC2000B, Blade
    # Initialise the first detected device
    chopper = MC2000B()
    # We'll assume the default MC1F10HP is installed
    print(chopper.get_blade_string())
    # Set up to use external reference source and the inner part of the blade
    chopper.set_inref_string("external-inner")
    # Apply a 1/2 divider to the input frequency
    chopper.nharmonic = 1
    chopper.dharmonic = 2
    # Start it up!
    chopper.enable = True

    # If a different chopper blade is installed, it can be configured by
    # using the Blade enum, for example for the MC1F60 model:
    chopper.blade = Blade.MC1F60
    # This may change the available input and/or output reference sources.
    # To check which are available for a blade model:
    print(Blade.MC1F60.inrefs)
    print(Blade.MC1F60.outrefs)


Support
-------

.. 
    Documentation can be found online at `https://thorlabs-mc2000b.readthedocs.io/en/latest/`_.

Bug reports, feature requests and suggestions can be submitted to the `issue tracker <https://gitlab.com/ptapping/thorlabs-mc2000b/-/issues>`_.


License
-------

All original work is free and open source, licensed under the GNU Public License.
See the `LICENSE.txt <https://gitlab.com/ptapping/thorlabs-apt-device/-/blob/main/LICENSE.txt>`_ for details.
