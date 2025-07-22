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

from enum import Enum
from typing import Collection

from bleak import BleakClient

from .constants import LEGO_CHARACTERISTIC_UUID
from .scanner import AdvertisedHub
from ..lwp3 import MessageType
from ..lwp3.encoding import encode_message, decode_message
from ..lwp3.enums import DeviceTypeID


class ConnectedHub:

    def __init__(self, name: str, client: BleakClient):
        self._name = name
        self._client = client
        self._ports = {}
        self.__connected = False

    @classmethod
    def from_advertised_hub(cls, advertised_hub: AdvertisedHub):
        return cls(advertised_hub.device.name, BleakClient(advertised_hub.device))

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        await self._client.connect()
        await self._client.start_notify(LEGO_CHARACTERISTIC_UUID, self._handle_notification)
        self.__connected = True

    async def disconnect(self):
        await self._client.disconnect()
        self.__connected = False

    async def send_bytes(self, payload: bytes):
        """Send payload to LEGO hub "as is".

        Args:
            payload: Data to be sent to LEGO hub.
        """
        await self._client.write_gatt_char(LEGO_CHARACTERISTIC_UUID, payload)

    async def send_message_bytes(self, message_type: MessageType, payload: bytes):
        """Send a message to LEGO hub.

        Args:
            message_type: Type of message to be sent to LEGO hub.
            payload: Message payload to be sent to LEGO hub.
        """
        message = encode_message(message_type, payload)
        await self.send_bytes(message)


    @property
    def name(self) -> str:
        return self._name

    def get_ports_with_devices(self, device_ids: Collection[DeviceTypeID]) -> list[int]:
        return [pid for pid, did in self._ports.items() if did in device_ids]

    def _handle_notification(self, _sender, data):
        message_type, payload = decode_message(data)
        if message_type is MessageType.HUB_ATTACHED_IO:
            # attach/detach of device
            port_id = payload[0]
            operation = DeviceOperationType(payload[1])
            device_type_id = payload[2]
            self._handle_device_change(port_id, operation, device_type_id)

    def _handle_device_change(self, port_id: int, operation: DeviceOperationType, device_type_id: int):
        if operation is DeviceOperationType.DETACH:
            try:
                self._ports.pop(port_id)
            except KeyError:
                # TODO: Log
                pass
        else:
            self._ports[port_id] = DeviceTypeID(device_type_id)


class DeviceOperationType(Enum):
    DETACH = 0x00
    ATTACH = 0x01
    ATTACH_VIRTUAL = 0x02
