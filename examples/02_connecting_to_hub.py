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

from blego.bt.connection import ConnectedHub
from blego.bt.scanner import HubScanner
from blego.lwp3 import MessageType
from blego.lwp3.enums import DeviceTypeID, Color

TIMEOUT = 5

async def main():
    """Creates an instance of the HubScanner and starts scanning for LEGO hubs.
    Connect to the first hub found and send a message to it.
    If all goes well, the hub should blink by its LED and if any motor is attached, it should start running.
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
        await change_led(hub)
        await run_motor(hub)
        await sleep(2)
        print("Disconnecting from hub...")
    print("Hub disconnected.")


async def change_led(hub):
    try:
        led_port = hub.get_ports_with_devices([DeviceTypeID.POWERED_UP_HUB_INDICATOR_LIGHT])[0]
    except IndexError:
        print("Hub does not have an indicator LED.")
        exit(1)

    msg_type = MessageType.PORT_INPUT_FORMAT_SETUP_SINGLE
    payload = bytes([led_port, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00])  # set color from enum
    await hub.send_message_bytes(msg_type, payload)

    msg_type = MessageType.PORT_OUTPUT_COMMAND

    print("Blinking the LED three times.")

    for _ in range(3):
        payload = bytes([led_port, 0b00010000, 0x51, 0x00, Color.GREEN])
        await hub.send_message_bytes(msg_type, payload)
        await sleep(1)
        payload = bytes([led_port, 0b00010000, 0x51, 0x00, Color.WHITE])  # back to white
        await hub.send_message_bytes(msg_type, payload)
        await sleep(1)


async def run_motor(hub):
    try:
        led_port = hub.get_ports_with_devices(DeviceTypeID.motors)[0]
    except IndexError:
        print("No motor attached to hub.")
        return

    msg_type = MessageType.PORT_OUTPUT_COMMAND
    payload = bytes([led_port, 0b00010000, 0x01, 50])  # set speed to 50%
    await hub.send_message_bytes(msg_type, payload)

    print("Motor is running.")
    await sleep(3)
    payload = bytes([led_port, 0x11, 0x07, 0])  # set speed to 0
    await hub.send_message_bytes(msg_type, payload)
    print("Motor stopped.")


if __name__ == "__main__":
    asyncio.run(main())
