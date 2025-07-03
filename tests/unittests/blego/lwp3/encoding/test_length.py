# -*- coding: utf-8 -*-
""" """

__copyright__ = "Copyright (c) 2025 MIL Innovation A/S. All Rights Reserved."

import pytest

from blego.lwp3 import MessageType
from blego.lwp3.encoding import encode_message


@pytest.mark.parametrize(
    "payload_length, expected_encoded_length",
    [
        (0, b"\x03"),  # empty payload. the total length of the message is 3
        (1, b"\x04"),  # one byte. the total length of the message is 4
        (2, b"\x05"),  # two bytes. the total length of the message is 5
        (124, b"\x7f"),  # the biggest payload encoded by 1 byte. the total length of the message is 127
        (125, b"\x82\x01"),  # the smallest payload encoded by 2 bytes. the total length of the message is 129
        (126, b"\x83\x01"),  # payload encoded by two bytes. the total length of the message is 130
    ]
)
def test_encode_message(payload_length, expected_encoded_length):
    """Test message length encoding.

    Note:
        I am not sure if messages longer than 127 bytes are encoded correctly.
    """
    payload = b'a' * payload_length
    expected = expected_encoded_length + b"\x00\x01" + payload

    encoded = encode_message(
        MessageType(0x01),  # randomly chosen message type
        payload
    )
    assert encoded == expected
