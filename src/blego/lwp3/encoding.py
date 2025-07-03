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

from blego.lwp3 import MessageType


def encode_message(message_type: MessageType, payload: bytes) -> bytes:
    """Encodes a message into a byte array."""
    without_length = bytes([
        0x00, # always zero
        message_type.value  # message payload
    ]) + payload

    if len(without_length) < 127:
        # the extra one is for the "length byte"
        return bytes([len(without_length) + 1]) + without_length
    else:
        length = len(without_length) + 2  # 2 is stands for 2 bytes of length
        lsb = length % 127
        msb = length // 127
        return bytes([0x80 | lsb, msb]) + without_length


def decode_message(message: bytes) -> tuple[MessageType, bytes]:
    """Decodes a message from a byte array."""
    if len(message) < 3:
        raise ValueError("Message is too short.")

    if 0x80 & message[0]:
        # the message is longer than 127 bytes
        message_type = MessageType(message[3])
        payload = message[4:]
    else:
        message_type = MessageType(message[2])
        payload = message[3:]
    return message_type, payload
