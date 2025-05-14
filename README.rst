
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ds18x20/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/ds18x20/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_DS18X20/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_DS18X20/actions/
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython driver for Dallas 1-Wire temperature sensor.

.. warning::
    Blinka for RPi / SBC does not currently support OneWire directly. However,
    you can use the `DS2482S-800 <https://github.com/adafruit/Adafruit_CircuitPython_DS248x>`_
    as an I2C to OneWire bridge, see: `Learn Guide <https://learn.adafruit.com/adafruit-ds2482s-800-8-channel-i2c-to-1-wire-bus-adapter/circuitpython-and-python>`_

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit OneWire <https://github.com/adafruit/Adafruit_CircuitPython_OneWire>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

.. code-block:: python

    import board
    from adafruit_onewire.bus import OneWireBus
    from adafruit_ds18x20 import DS18X20

    ow_bus = OneWireBus(board.D2)
    ds18 = DS18X20(ow_bus, ow_bus.scan()[0])
    ds18.temperature


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/ds18x20/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_DS18X20/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
