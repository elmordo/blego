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

from asyncio import Task, Queue, create_task, sleep
from dataclasses import dataclass
from typing import AsyncIterable

from bleak import BLEDevice, AdvertisementData, BleakScanner

from .constants import LEGO_SERVICE_UUID


class HubScanner:

    def __init__(self):
        self._scanner = BleakScanner(self._detected, [LEGO_SERVICE_UUID])
        self._discovered_devices: list[AdvertisedHub] = []
        self._scanning = False
        self._timeout_task: Task | None = None
        self._queue = Queue()

    def get_discovered_devices(self) -> list[AdvertisedHub]:
        return self._discovered_devices.copy()

    async def start(self, timeout: float | None = 5.0) -> AsyncIterable[AdvertisedHub]:
        self._discovered_devices = []
        self._queue = Queue()
        self._scanning = True
        await self._scanner.start()

        if timeout is not None:
            self._set_timeout(timeout)

        return self._make_generator()

    async def stop(self):
        if self._scanning:
            self._scanning = False
            await self._scanner.stop()

        # clear the timeout task
        if self._timeout_task and not self._timeout_task.done():
            self._timeout_task.cancel("Cancelled by user")
        self._timeout_task = None
        self._queue.put_nowait(None)
        await self._queue.join()

    def _detected(self, device, advertisement_data):
        # add info into the discovered devices
        hub_info = AdvertisedHub(device, advertisement_data)
        self._discovered_devices.append(hub_info)
        self._queue.put_nowait(hub_info)

    def _set_timeout(self, timeout: float):
        self._timeout_task = create_task(self._stop_after_timeout(timeout))

    def _make_generator(self) -> AsyncIterable[AdvertisedHub]:
        async def generator():
            while True:
                item = await self._queue.get()
                self._queue.task_done()
                if item is None:
                    break
                yield item

        return generator()

    async def _stop_after_timeout(self, timeout: float):
        await sleep(timeout)
        if self._scanning:
            await self.stop()


@dataclass()
class AdvertisedHub:
    device: BLEDevice
    data: AdvertisementData
