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
import asyncio
from asyncio import sleep

from blego.hub import LegoHub
from blego_bt_server.connection import ConnectedHub
from blego_bt_server.scanner import HubScanner


TIMEOUT = 5

async def main():
    """Creates an instance of the HubScanner and starts scanning for LEGO hubs.
    Connect to the first hub found and send a message to it.
    If all goes well, the hub should blink by its LED.
    """
    scanner = HubScanner()
    print(f"Searching for LEGO hubs for {TIMEOUT} seconds...")
    async for advertised_hub in await scanner.start(5):
        print("Hub found: ", advertised_hub)
        break
    else:
        print("No hubs found.")
        exit(1)

    print("Search completed.")
    print("Connecting to hub...")
    hub = ConnectedHub.from_advertised_hub(advertised_hub)
    print("Hub connected.")

    async with hub:
        await sleep(2)
        print("Disconnecting from hub...")
    print("Hub disconnected.")


if __name__ == "__main__":
    asyncio.run(main())
