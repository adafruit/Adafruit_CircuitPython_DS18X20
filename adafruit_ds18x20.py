# The MIT License (MIT)
#
# Copyright (c) 2017 Carter Nelson for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_ds18x20`
====================================================

Driver for Dallas 1-Wire temperature sensor.

* Author(s): Carter Nelson
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_DS18x20.git"

import time
from adafruit_onewire.device import OneWireDevice
from micropython import const

_CONVERT = b'\x44'
_RD_SCRATCH = b'\xBE'
_WR_SCRATCH = b'\x4E'
_CONVERSION_TIMEOUT = const(1)
RESOLUTION = (9, 10, 11, 12)

class DS18X20(object):
    """Class which provides interface to DS18X20 temperature sensor."""

    def __init__(self, bus, address):
        if address.family_code == 0x10 or address.family_code == 0x28:
            self._address = address
            self._device = OneWireDevice(bus, address)
            self._buf = bytearray(9)
        else:
            raise ValueError('Incorrect family code in device address.')

    @property
    def temperature(self):
        """The temperature in degrees Celsius."""
        self._convert_temp()
        return self._read_temp()

    @property
    def resolution(self):
        """The programmable resolution. 9, 10, 11, or 12 bits."""
        return RESOLUTION[self._read_scratch()[4] >> 5 & 0x03]

    @resolution.setter
    def resolution(self, bits):
        if bits not in RESOLUTION:
            raise ValueError('Incorrect resolution. Must be 9, 10, 11, or 12.')
        self._buf[0] = 0  # TH register
        self._buf[1] = 0  # TL register
        self._buf[2] = RESOLUTION.index(bits) << 5 | 0x1F # configuration register
        self._write_scratch(self._buf)

    def _convert_temp(self, timeout=_CONVERSION_TIMEOUT):
        with self._device as dev:
            dev.write(_CONVERT)
            start_time = time.monotonic()
            if timeout > 0:
                dev.readinto(self._buf, end=1)
                # 0 = conversion in progress, 1 = conversion done
                while self._buf[0] == 0x00:
                    if time.monotonic() - start_time > timeout:
                        raise RuntimeError('Timeout waiting for conversion to complete.')
                    dev.readinto(self._buf, end=1)
        return time.monotonic() - start_time

    def _read_temp(self):
        # pylint: disable=invalid-name
        buf = self._read_scratch()
        if self._address.family_code == 0x10:
            if buf[1]:
                t = buf[0] >> 1 | 0x80
                t = -((~t + 1) & 0xff)
            else:
                t = buf[0] >> 1
            return t - 0.25 + (buf[7] - buf[6]) / buf[7]
        else:
            t = buf[1] << 8 | buf[0]
            if t & 0x8000: # sign bit set
                t = -((t ^ 0xffff) + 1)
            return t / 16

    def _read_scratch(self):
        with self._device as dev:
            dev.write(_RD_SCRATCH)
            dev.readinto(self._buf)
        return self._buf

    def _write_scratch(self, buf):
        with self._device as dev:
            dev.write(_WR_SCRATCH)
            dev.write(buf, end=3)
