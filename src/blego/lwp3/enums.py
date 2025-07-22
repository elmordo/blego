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

from enum import IntEnum
from typing import Self


class MessageType(IntEnum):
    """Message types defined by the LWP3"""

    # Message Type Definitions - HUB related

    HUB_PROPERTIES = 0x01
    """Set or retrieve standard Hub property information, such as name or battery status"""

    HUB_ACTIONS = 0x02
    """Perform specific actions on the hub, like forcing shutdown or restarting"""

    HUB_ALERTS = 0x03
    """Manage or fetch hub alerts, such as low battery notifications"""

    HUB_ATTACHED_IO = 0x04
    """Sent when the hub detects IO devices being attached"""

    GENERIC_ERROR_MESSAGES = 0x05
    """Communicate generic errors from the hub"""

    HW_NETWORK_COMMANDS = 0x08
    """Commands used for hardware network configuration"""

    FW_UPDATE_BOOT_MODE = 0x10
    """Switch the hub to a special firmware update (boot loader) mode"""

    FW_UPDATE_LOCK_MEMORY = 0x11
    """Lock the hub memory (used during firmware updates)"""

    FW_UPDATE_LOCK_STATUS_REQUEST = 0x12
    """Request the current memory lock status of the hub"""

    FW_LOCK_STATUS = 0x13
    """Response with the hub's memory lock status"""

    # Port-related message types

    PORT_INFO_REQUEST = 0x21
    """Request basic information about a hub port"""

    PORT_MODE_INFO_REQUEST = 0x22
    """Request detailed information about specific port modes"""

    PORT_INPUT_FORMAT_SETUP_SINGLE = 0x41
    """Configure input format for a single port mode"""

    PORT_INPUT_FORMAT_SETUP_COMBINED = 0x42
    """Configure input format for combined (multi-mode) ports"""

    PORT_INFO = 0x43
    """Response with information about a hub port"""

    PORT_MODE_INFO = 0x44
    """Response with detailed information about specific port modes"""

    PORT_VALUE_SINGLE = 0x45
    """Transmit value updates for a single port mode"""

    PORT_VALUE_COMBINED = 0x46
    """Transmit value updates for multiple port modes in combined mode"""

    PORT_INPUT_FORMAT_SINGLE = 0x47
    """Retrieve or set input format for a single port mode"""

    PORT_INPUT_FORMAT_COMBINED = 0x48
    """Retrieve or set input format for combined port modes"""

    VIRTUAL_PORT_SETUP = 0x61
    """Manage synchronization between virtual (logical) ports"""

    PORT_OUTPUT_COMMAND = 0x81
    """Send output commands to a specific port (e.g., motor control)"""

    PORT_OUTPUT_COMMAND_FEEDBACK = 0x82
    """Receive feedback on executed output commands"""


class HubPropertyReference(IntEnum):
    """
    Hub Property Reference - matches UInt8 values to specific hub property names
    """

    ADVERTISING_NAME = 0x01
    """Name broadcasted by the hub (Upstream/Downstream)"""

    BUTTON = 0x02
    """Button state on the hub (Upstream)"""

    FW_VERSION = 0x03
    """Current firmware version (Upstream)"""

    HW_VERSION = 0x04
    """Current hardware version (Upstream)"""

    RSSI = 0x05
    """Hub's signal strength as received by a connected device (Upstream)"""

    BATTERY_VOLTAGE = 0x06
    """Current battery charge percentage (Upstream)"""

    BATTERY_TYPE = 0x07
    """Type of battery (e.g., normal or rechargeable) (Upstream)"""

    MANUFACTURER_NAME = 0x08
    """Manufacturer's name (e.g., LEGO) (Upstream)"""

    RADIO_FIRMWARE_VERSION = 0x09
    """Firmware version of the internal radio (Upstream)"""

    LEGO_WIRELESS_PROTOCOL_VERSION = 0x0A
    """Version of the wireless protocol in use (Upstream)"""

    SYSTEM_TYPE_ID = 0x0B
    """A unique identifier for the hub's system type (Upstream)"""

    HW_NETWORK_ID = 0x0C
    """Current hardware network ID (Upstream)"""

    PRIMARY_MAC_ADDRESS = 0x0D
    """MAC address used for BLE communication (Upstream)"""

    SECONDARY_MAC_ADDRESS = 0x0E
    """MAC address used by the Boot Loader task (Upstream)"""

    HW_NETWORK_FAMILY = 0x0F
    """Family identifier for hardware networks (0-8) (Upstream)"""


class HubPropertyOperation(IntEnum):
    """
    Hub Property Operation - matches UInt8 values to hub property operations
    """

    SET = 0x01
    """Set a property value (Downstream)"""
    ENABLE_UPDATES = 0x02
    """Enable automatic updates for a property (Downstream)"""
    DISABLE_UPDATES = 0x03
    """Disable automatic updates for a property (Downstream)"""
    RESET = 0x04
    """Reset a property to its default value (Downstream)"""
    REQUEST_UPDATE = 0x05
    """Request the current value of a property (Downstream)"""
    UPDATE = 0x06
    """Notify that a property has been updated (Upstream)"""


class HubActionType(IntEnum):
    """
    Hub Action Type - defines downstream and upstream actions executable by the hub or its clients.
    """

    # Downstream actions (reserved 0x00–0x2F)
    SWITCH_OFF_HUB = 0x01
    """Switch Off Hub"""
    DISCONNECT = 0x02
    """Disconnect"""
    VCC_PORT_CONTROL_ON = 0x03
    """VCC Port Control On"""
    VCC_PORT_CONTROL_OFF = 0x04
    """VCC Port Control Off"""
    ACTIVATE_BUSY_INDICATION = 0x05
    """Activate BUSY Indication (Shown by RGB. Actual RGB settings preserved)."""
    RESET_BUSY_INDICATION = 0x06
    """Reset BUSY Indication (RGB shows the previously preserved RGB settings)."""
    # Additional actions placeholders
    SHUTDOWN_FAST = 0x2F
    """Shutdown the Hub without any upstream information sent. Suggested for production use only."""

    # Upstream actions (reserved 0x30–0x64)
    HUB_WILL_SWITCH_OFF = 0x30
    """Hub Will Switch Off"""
    HUB_WILL_DISCONNECT = 0x31
    """Hub Will Disconnect"""
    HUB_WILL_GO_INTO_BOOT_MODE = 0x32
    """Hub Will Go Into Boot Mode"""


class AlertType(IntEnum):
    """
    Hub Alert Types - matches UInt8 values to specific alert types
    """

    LOW_VOLTAGE = 0x01
    """Low Voltage"""
    HIGH_CURRENT = 0x02
    """High Current"""
    LOW_SIGNAL_STRENGTH = 0x03
    """Low Signal Strength"""
    OVER_POWER_CONDITION = 0x04
    """Over Power Condition"""


class AlertOperation(IntEnum):
    """
    Hub Alert Operations - matches UInt8 values to specific alert operations
    """

    ENABLE_UPDATES = 0x01
    """Enable Updates (Downstream)"""
    DISABLE_UPDATES = 0x02
    """Disable Updates (Downstream)"""
    REQUEST_UPDATES = 0x03
    """Request Updates (Downstream)"""
    UPDATE = 0x04
    """Update (Upstream)"""


class AlertPayload(IntEnum):
    """
    Hub Alert Message Payload in the upstream direction
    """

    STATUS_OK = 0x00
    """Status OK"""
    ALERT = 0xFF
    """Alert!"""


class IOEvent(IntEnum):
    """
    I/O Event - matches UInt8 values to specific I/O events
    """

    DETACHED_IO = 0x00
    """Detached I/O"""
    ATTACHED_IO = 0x01
    """Attached I/O"""
    ATTACHED_VIRTUAL_IO = 0x02
    """Attached Virtual I/O"""


class DeviceTypeID(IntEnum):
    """
    Device Type ID - Defines various device types with their unique identifiers.

    Source: https://github.com/pybricks/technical-info/blob/master/assigned-numbers.md
    """

    POWERED_UP_MEDIUM_MOTOR = 0x01
    """Powered Up Medium Motor (45303, 21980)"""

    POWERED_UP_TRAIN_MOTOR = 0x02
    """Powered Up Train Motor (88011, bb0896c01)"""

    POWERED_UP_LIGHTS = 0x08
    """Powered Up Lights (88005, 22168c01)"""

    POWERED_UP_HUB_BATTERY_VOLTAGE = 0x14
    """Powered Up Hub battery voltage (N/A)"""

    POWERED_UP_HUB_BATTERY_CURRENT = 0x15
    """Powered Up Hub battery current (N/A)"""

    POWERED_UP_HUB_PIEZO_TONE = 0x16
    """Powered Up Hub piezo tone (N/A)"""

    POWERED_UP_HUB_INDICATOR_LIGHT = 0x17
    """Powered Up Hub indicator light (N/A)"""

    EV3_COLOR_SENSOR = 0x1D
    """EV3 Color Sensor (45506, retired, 95650)"""

    EV3_ULTRASONIC_SENSOR = 0x1E
    """EV3 Ultrasonic Sensor (45504, retired, 95652)"""

    EV3_GYRO_SENSOR = 0x20
    """EV3 Gyro Sensor (45505, retired, 99380)"""

    EV3_INFRARED_SENSOR = 0x21
    """EV3 Infrared Sensor (45509, retired, 95654)"""

    WEDO_2_TILT_SENSOR = 0x22
    """WeDo 2.0 Tilt Sensor (45305, 20841)"""

    WEDO_2_MOTION_SENSOR = 0x23
    """WeDo 2.0 Motion Sensor (45304, 20844)"""

    WEDO_2_GENERIC_DEVICE = 0x24
    """WeDo 2.0 generic device (N/A)"""

    BOOST_COLOR_DISTANCE_SENSOR = 0x25
    """BOOST Color and Distance Sensor (88007, bb0891c01)"""

    BOOST_INTERACTIVE_MOTOR = 0x26
    """BOOST Interactive Motor (88008, bb0893c01)"""

    BOOST_MOVE_HUB_BUILT_IN_MOTOR = 0x27
    """BOOST Move Hub built-in motor (N/A)"""

    BOOST_MOVE_HUB_ACCELEROMETER = 0x28
    """BOOST Move Hub built-in accelerometer (tilt sensor, N/A)"""

    DUPLO_TRAIN_HUB_BUILT_IN_MOTOR = 0x29
    """DUPLO Train hub built-in motor (N/A)"""

    DUPLO_TRAIN_HUB_BUILT_IN_BEEPER = 0x2A
    """DUPLO Train hub built-in beeper (N/A)"""

    DUPLO_TRAIN_HUB_COLOR_SENSOR = 0x2B
    """DUPLO Train hub built-in color sensor (N/A)"""

    DUPLO_TRAIN_HUB_SPEED = 0x2C
    """DUPLO Train hub built-in speed (N/A)"""

    TECHNIC_CONTROL_PLUS_LARGE_MOTOR = 0x2E
    """Technic Control+ Large Motor (88013, bb0959c01)"""

    TECHNIC_CONTROL_PLUS_XL_MOTOR = 0x2F
    """Technic Control+ XL Motor (88014, bb0960c01)"""

    SPIKE_PRIME_MEDIUM_MOTOR = 0x30
    """SPIKE Prime Medium Motor (45603, 54696c01)"""

    SPIKE_PRIME_LARGE_MOTOR = 0x31
    """SPIKE Prime Large Motor (45602, 54675c01)"""

    TECHNIC_CONTROL_PLUS_HUB = 0x32
    """Technic Control+ Hub (N/A)"""

    POWERED_UP_HUB_IMU_GESTURE = 0x36
    """Powered Up hub IMU gesture (N/A)"""

    POWERED_UP_HANDSET_BUTTONS = 0x37
    """Powered Up Handset Buttons (N/A)"""

    POWERED_UP_HUB_BLUETOOTH_RSSI = 0x38
    """Powered Up hub Bluetooth RSSI (N/A)"""

    POWERED_UP_HUB_ACCELEROMETER = 0x39
    """Powered Up hub IMU accelerometer (N/A)"""

    POWERED_UP_HUB_GYRO = 0x3A
    """Powered Up hub IMU gyro (N/A)"""

    POWERED_UP_HUB_IMU_POSITION = 0x3B
    """Powered Up hub IMU position (N/A)"""

    POWERED_UP_HUB_IMU_TEMPERATURE = 0x3C
    """Powered Up hub IMU temperature (N/A)"""

    TECHNIC_COLOR_SENSOR = 0x3D
    """Technic Color Sensor (45605, 37308c01)"""

    TECHNIC_ULTRASONIC_DISTANCE_SENSOR = 0x3E
    """Technic Ultrasonic/Distance Sensor (45604, 37316c01)"""

    TECHNIC_FORCE_SENSOR = 0x3F
    """Technic Force Sensor (45606, 37312c01)"""

    TECHNIC_LIGHT_MATRIX = 0x40
    """Technic 3x3 Color Light Matrix (45608, 47592c01)"""

    TECHNIC_SMALL_ANGULAR_MOTOR = 0x41
    """Technic Small Angular Motor (45607, 68488c01)"""

    MARIO_BUILT_IN_UNKNOWN = 0x46
    """Mario built-in unknown (N/A)"""

    MARIO_IMU_SENSOR = 0x47
    """Mario built-in IMU gesture sensor (N/A)"""

    MARIO_COLOR_BARCODE_SENSOR = 0x49
    """Mario built-in color barcode sensor (N/A)"""

    MARIO_PANTS_SENSOR = 0x4A
    """Mario built-in pants sensor (N/A)"""

    TECHNIC_MEDIUM_ANGULAR_MOTOR_GRAY = 0x4B
    """Technic Medium Angular Motor, gray (88018, 54696c01)"""

    TECHNIC_LARGE_ANGULAR_MOTOR_GRAY = 0x4C
    """Technic Large Angular Motor, gray (88017, 54675c02)"""

    TECHNIC_MOVE_HUB_DRIVE_MOTOR = 0x56
    """Technic Move hub built-in drive motor (N/A)"""

    TECHNIC_MOVE_HUB_STEERING_MOTOR = 0x57
    """Technic Move hub built-in steering motor (N/A)"""

    TECHNIC_MOVE_HUB_LIGHTS = 0x58
    """Technic Move hub built-in lights (6, N/A)"""

    POWERED_UP_HUB_IMU_ORIENTATION = 0x5D
    """Powered Up hub IMU orientation (N/A)"""

    POWERED_UP_HUB_UNKNOWN = 0x5E
    """Powered Up hub unknown (GEST_BITMAP)"""

    @classmethod
    @property
    def motors(cls) -> set[Self]:
        return {
            cls.POWERED_UP_MEDIUM_MOTOR,
            cls.POWERED_UP_TRAIN_MOTOR,
            cls.BOOST_INTERACTIVE_MOTOR,
            cls.BOOST_MOVE_HUB_BUILT_IN_MOTOR,
            cls.DUPLO_TRAIN_HUB_BUILT_IN_MOTOR,
            cls.TECHNIC_CONTROL_PLUS_LARGE_MOTOR,
            cls.TECHNIC_CONTROL_PLUS_XL_MOTOR,
            cls.SPIKE_PRIME_MEDIUM_MOTOR,
            cls.SPIKE_PRIME_LARGE_MOTOR,
            cls.TECHNIC_MEDIUM_ANGULAR_MOTOR_GRAY,
            cls.TECHNIC_LARGE_ANGULAR_MOTOR_GRAY,
            cls.TECHNIC_MOVE_HUB_DRIVE_MOTOR,
            cls.TECHNIC_MOVE_HUB_STEERING_MOTOR,
        }


class ErrorCode(IntEnum):
    """
    Error Code - Defines various error codes and their descriptions
    """

    ACK = 0x01
    """Acknowledged"""

    MACK = 0x02
    """Message Acknowledged"""

    BUFFER_OVERFLOW = 0x03
    """Buffer Overflow"""

    TIMEOUT = 0x04
    """Timeout"""

    COMMAND_NOT_RECOGNIZED = 0x05
    """Command NOT recognized"""

    INVALID_USE = 0x06
    """Invalid use (e.g., parameter error(s))"""

    OVERCURRENT = 0x07
    """Overcurrent"""

    INTERNAL_ERROR = 0x08
    """Internal ERROR"""


class HWNetWorkCommand(IntEnum):
    """
    H/W Network Command Types - Defines hardware network-related commands and their values
    """

    CONNECTION_REQUEST = 0x02
    """Connection Request"""

    FAMILY_REQUEST = 0x03
    """Family Request [New family if available]"""

    FAMILY_SET = 0x04
    """Family Set"""

    JOIN_DENIED = 0x05
    """Join Denied"""

    GET_FAMILY = 0x06
    """Get Family"""

    FAMILY = 0x07
    """Family"""

    GET_SUBFAMILY = 0x08
    """Get SubFamily"""

    SUBFAMILY = 0x09
    """SubFamily"""

    SUBFAMILY_SET = 0x0A
    """SubFamily Set"""

    GET_EXTENDED_FAMILY = 0x0B
    """Get Extended Family"""

    EXTENDED_FAMILY = 0x0C
    """Extended Family"""

    EXTENDED_FAMILY_SET = 0x0D
    """Extended Family Set"""

    RESET_LONG_PRESS_TIMING = 0x0E
    """Reset Long Press Timing"""


class HWFamilyLedColour(IntEnum):
    """
    H/W Network Families Predefined LED Colors - matches UInt8 values to LED color codes.
    """

    FAMILY_0_WHITE = 0x00
    """Family 0 (zero) - White"""

    FAMILY_1_GREEN = 0x01
    """Family 1 - Green"""

    FAMILY_2_YELLOW = 0x02
    """Family 2 - Yellow"""

    FAMILY_3_RED = 0x03
    """Family 3 - Red"""

    FAMILY_4_BLUE = 0x04
    """Family 4 - Blue"""

    FAMILY_5_PURPLE = 0x05
    """Family 5 - Purple"""

    FAMILY_6_LIGHT_BLUE = 0x06
    """Family 6 - Light Blue"""

    FAMILY_7_TEAL = 0x07
    """Family 7 - Teal"""

    FAMILY_8_PINK = 0x08
    """Family 8 - Pink"""


class HWSubFamilyLedFlashes(IntEnum):
    """
    H/W Network Families (Flashes) - Defines flash patterns for sub-families.
    """

    SUB_FAMILY_1_ONE_FLASH = 0x01
    """Sub-Family 1 - One Flash"""

    SUB_FAMILY_2_TWO_FLASHES = 0x02
    """Sub-Family 2 - Two Flashes"""

    SUB_FAMILY_3_THREE_FLASHES = 0x03
    """Sub-Family 3 - Three Flashes"""

    SUB_FAMILY_4_FOUR_FLASHES = 0x04
    """Sub-Family 4 - Four Flashes"""

    SUB_FAMILY_5_FIVE_FLASHES = 0x05
    """Sub-Family 5 - Five Flashes"""

    SUB_FAMILY_6_SIX_FLASHES = 0x06
    """Sub-Family 6 - Six Flashes"""

    SUB_FAMILY_7_SEVEN_FLASHES = 0x07
    """Sub-Family 7 - Seven Flashes"""


class PortInformationType(IntEnum):
    """
    Port Information Type - corresponds UInt8 values to the type of information requested or transmitted about a port
    """

    PORT_VALUE = 0x00
    """Retrieve the current value of the port"""

    MODE_INFO = 0x01
    """Request or provide detailed information about modes that can be used on this port"""

    POSSIBLE_MODE_COMBINATIONS = 0x02
    """
    Request or provide information about possible mode combinations.
    Should only be used if the “Logical Combinable”-bit is set in the MODE INFO Capabilities byte.
    See details in Port Information 0x43.
    """


class PortModeInformationType(IntEnum):
    """
    Port Mode Information Type - Corresponds UInt8 values to mode information for a given port in LWP3
    """

    NAME = 0x00
    """Name of the mode"""

    RAW = 0x01
    """The raw range values"""

    PCT = 0x02
    """The percent range values"""

    SI = 0x03
    """The SI (standard international) value range"""

    SYMBOL = 0x04
    """The standard name of value"""

    MAPPING = 0x05
    """Mapping information used internally"""

    MOTOR_BIAS = 0x07
    """Motor Bias (0–100%)"""

    CAPABILITIES = 0x08
    """Capability bits (6 bytes total)"""

    VALUE_FORMAT = 0x80
    """Value format and encoding information"""


class PortInputFormatSetupCommand(IntEnum):
    """
    Port Input Format Setup Command - corresponds UInt8 values to command actions
    """

    SET_MODE_AND_DATASET_COMBINATIONS = 0x01
    """Set Mode and Dataset combinations"""

    LOCK_LPF2_DEVICE_FOR_SETUP = 0x02
    """Lock LPF2 Device for setup"""

    UNLOCK_AND_START_WITH_MULTI_UPDATE_ENABLED = 0x03
    """Unlock and start with multi-update enabled"""

    UNLOCK_AND_START_WITH_MULTI_UPDATE_DISABLED = 0x04
    """Unlock and start with multi-update disabled"""

    RESET_SENSOR = 0x06
    """Reset sensor"""


class PossibleModeCombination(IntEnum):
    """
    Possible Mode Combinations - Maps binary indices to mode combinations.
    """

    MODE_1_2_4 = 0b0000000000001011
    """Index 0: Mode 1 + Mode 2 + Mode 4"""

    MODE_0_1 = 0b0000000000000011
    """Index 1: Mode 0 + Mode 1"""

    MODE_0_3 = 0b0000000000010001
    """Index 2: Mode 0 + Mode 3"""

    @staticmethod
    def is_valid_mode(mode: int) -> bool:
        """
        Check if the provided integer is a valid mode.

        :param mode: Integer to check.
        :return: True if it matches one of the predefined modes, otherwise False.
        """
        return mode in {item.value for item in PossibleModeCombination}


class Color(IntEnum):
    BLACK = 0
    PINK = 1
    PURPLE = 2
    BLUE = 3
    LIGHTBLUE = 4
    CYAN = 5
    GREEN = 6
    YELLOW = 7
    ORANGE = 8
    RED = 9
    WHITE = 10
    NONE = 11
