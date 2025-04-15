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

from abc import ABC, abstractmethod
from typing import Self

from .enums import MessageType, HubPropertyReference, HubPropertyOperation


class Message(ABC):

    @abstractmethod
    def get_message_type(self) -> MessageType:
        pass

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> Self:
        """The message content without the message header (the first three bytes)"""
        raise NotImplementedError()


class HubMessage(Message, ABC):

    @abstractmethod
    def encode(self) -> bytes:
        pass


class HubProperties(HubMessage):
    """

    Up+Down
    """

    MAX_NAME_SIZE = 14

    def __init__(
        self,
        prop: HubPropertyReference,
        op: HubPropertyOperation,
        payload: bytes = b"",
    ):
        self.property = prop
        self.operation = op
        self.payload = payload

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        return cls(
            prop=HubPropertyReference(data[0]),
            op=HubPropertyOperation(data[1]),
            payload=data[2:],
        )

    @classmethod
    def new_set_advertising_name(cls, name: str) -> Self:
        payload = name.encode("utf-8")

        if len(payload) > cls.MAX_NAME_SIZE:
            raise ValueError(
                f"Max length of name is {cls.MAX_NAME_SIZE} bytes. Got {len(payload)} bytes instead."
            )

        return cls(
            prop=HubPropertyReference.ADVERTISING_NAME,
            op=HubPropertyOperation.SET,
            payload=payload,
        )

    def get_message_type(self) -> MessageType:
        return MessageType.HUB_PROPERTIES

    def encode(self) -> bytes:
        return bytes([self.property.value, self.operation.value]) + self.payload


class HubActions(HubMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.HUB_ACTIONS

    def encode(self) -> bytes:
        raise NotImplementedError


class HubAlerts(HubMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.HUB_ALERTS

    def encode(self) -> bytes:
        raise NotImplementedError


class HubAttachedIO(HubMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.HUB_ATTACHED_IO

    def encode(self) -> bytes:
        raise NotImplementedError


class GenericErrorMessages(HubMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.GENERIC_ERROR_MESSAGES

    def encode(self) -> bytes:
        raise NotImplementedError


class HWNetworkCommands(HubMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.HW_NETWORK_COMMANDS

    def encode(self) -> bytes:
        raise NotImplementedError


class FWUpdateBootMode(HubMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.FW_UPDATE_BOOT_MODE

    def encode(self) -> bytes:
        raise NotImplementedError


class FWUpdateLockMemory(HubMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.FW_UPDATE_LOCK_MEMORY

    def encode(self) -> bytes:
        raise NotImplementedError


class FWUpdateLockStatusRequest(HubMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.FW_UPDATE_LOCK_STATUS_REQUEST

    def encode(self) -> bytes:
        raise NotImplementedError


class FWLockStatus(HubMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.FW_LOCK_STATUS

    def encode(self) -> bytes:
        raise NotImplementedError


class PortMessage(Message, ABC):

    @abstractmethod
    def encode(self, port_id: int) -> bytes:
        pass


class PortInfoRequest(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_INFO_REQUEST

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortModeInfoRequest(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_MODE_INFO_REQUEST

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortInputFormatSetupSingle(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_INPUT_FORMAT_SETUP_SINGLE

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortInputFormatSetupCombined(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_INPUT_FORMAT_SETUP_COMBINED

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortInfo(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_INFO

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortModeInfo(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_MODE_INFO

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortValueSingle(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_VALUE_SINGLE

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortValueCombined(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_VALUE_COMBINED

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortInputFormatSingle(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_INPUT_FORMAT_SINGLE

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortInputFormatCombined(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_INPUT_FORMAT_COMBINED

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class VirtualPortSetup(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.VIRTUAL_PORT_SETUP

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortOutputCommand(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_OUTPUT_COMMAND

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError


class PortOutputCommandFeedback(PortMessage):
    def get_message_type(self) -> MessageType:
        return MessageType.PORT_OUTPUT_COMMAND_FEEDBACK

    def encode(self, port_id: int) -> bytes:
        raise NotImplementedError
