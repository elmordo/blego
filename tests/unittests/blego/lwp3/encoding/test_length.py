# -*- coding: utf-8 -*-
""" """

__copyright__ = "Copyright (c) 2025 MIL Innovation A/S. All Rights Reserved."

import pytest

from blego.lwp3.encoding import encode_length, decode_length


@pytest.mark.parametrize(
    "data, expected",
    [
        (1, bytes([0b0000_0001])),
        (128, bytes([0b1000_0000, 0b0000_0001])),
        (129, bytes([0b1000_0001, 0b0000_0001])),
        (130, bytes([0b1000_0010, 0b0000_0001])),
    ],
)
def test_encode_length(data, expected):
    assert encode_length(data) == expected, f"Expected {expected} but got {encode_length(data)}"


@pytest.mark.parametrize(
    "expected, data",
    [
        (1, bytes([0b0000_0001])),
        (128, bytes([0b1000_0000, 0b0000_0001])),
        (129, bytes([0b1000_0001, 0b0000_0001])),
        (130, bytes([0b1000_0010, 0b0000_0001])),
    ],
)
def test_decode_length(data, expected):
    assert decode_length(data) == expected, f"Expected {expected} but got {decode_length(data)}"
