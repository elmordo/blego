# MIT License
#
# Copyright (c) [YEAR] [COPYRIGHT HOLDER]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from enum import Enum, auto

import bleak
from bleak import BleakClient

from blego.lwp3.enums import DeviceTypeID


class HubScanner:

    def __init__(self):
        self._scanner = bleak.BleakScanner(self._detected, [LegoHub.SERVICE_UUID])

    async def start(self):
        await self._scanner.start()

    async def stop(self):
        await self._scanner.stop()

    def _detected(self, device, advertisement_data):
        print(device, advertisement_data)


class LegoHub:

    SERVICE_UUID = "00001623-1212-efde-1623-785feabcd123"

    def __init__(self, name: str, client: BleakClient):
        self._name = name
        self._ports = []

    @property
    def name(self) -> str:
        return self._name


class Port:

    def __init__(self, idx: int):
        self._idx = idx
        self._kind = PortKind.PHYSICAL if idx < 50 else PortKind.VIRTUAL
        self._status = PortStatus.UNKNOWN
        self._attached_device_type: DeviceTypeID | None = None

    @property
    def idx(self) -> int:
        return self._idx

    @property
    def kind(self) -> PortKind:
        return self._kind

    @property
    def status(self) -> PortStatus:
        return self._status

    @property
    def attached_device_type(self) -> DeviceTypeID | None:
        return self._attached_device_type


class PortStatus(Enum):
    ATTACHED = auto()
    DETACHED = auto()
    UNKNOWN = auto()
    """The status was not checked yet"""


class PortKind(Enum):
    VIRTUAL = auto()
    PHYSICAL = auto()
