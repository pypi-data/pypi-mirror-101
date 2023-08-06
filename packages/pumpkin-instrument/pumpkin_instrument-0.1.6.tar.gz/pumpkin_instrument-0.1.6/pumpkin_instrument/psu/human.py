# coding: utf-8
# ##############################################################################
#  (C) Copyright 2020 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""
This module contains the implementation for the Korad KD3005P PSU remote control.
Uses PySerial to control the PSU.
"""
from typing import ContextManager, List, Any
from contextlib import contextmanager

from .types import PowerSupply, PowerSupplyCapability, PowerSupplyChannelCapability, \
    PowerSupplyProtectionMode
from ..types import InstrumentType
from ..instrument import Instrument


class _HumanPowerSupplyContext(PowerSupply):
    """Initializes the Human Power Supply context"""

    def set_output_ocp(self, channel: int, is_on: bool):
        """Asks the user to turn ON or OFF OCP"""
        on_off = "ON" if is_on else "OFF"
        print(f"Turn the OCP protection {on_off} on the PSU.")
        input("Press <Enter> when done.")

    def set_output_ovp(self, channel: int, value: float):
        """Asks the user to set the OCV value on the PSU"""
        print(f"Set the OCV to {value:.3f} Volts.")
        input("Press <Enter> when done.")

    def set_output_voltage(self, channel: int, voltage: float):
        """Asks the user to set the output voltage on the PSU"""
        print(f"Set the output Voltage on Channel #{channel+1} to {voltage:.3f} Volts")
        input("Press <Enter> when done.")

    def set_output_current(self, channel: int, current: float):
        """Asks the user to set the output current on the PSU"""
        print(f"Set the output Current on Channel #{channel + 1} to {current:.3f} Amps")
        input("Press <Enter> when done.")

    def get_output_voltage(self, channel: int) -> float:
        """Asks the user to input the output voltage on the PSU"""
        while True:
            try:
                return float(input("Please enter the Voltage displayed on the PSU (V): "))
            except ValueError:
                # Keep going til they give us good stuff
                pass

    def get_output_current(self, channel: int) -> float:
        """
        Gets the output current of the KORAD.

        :param channel: Ignored
        :return: The actual output current.
        """
        while True:
            try:
                return float(input("Please enter the Current displayed on the PSU (A): "))
            except ValueError:
                # Keep going til they give us good stuff
                pass

    def clear_errors(self):
        """Asks the user to clear the errors"""
        input("Please clear any errors on the PSU. Press <Enter> when done.")

    def clear_faults(self):
        """Asks the user to clear the faults."""
        input("Please clear any faults on the PSU. Press <Enter> when done.")

    @property
    def error_count(self) -> int:
        """Human PSU just returns 0 for faults/errors"""
        # Just say there is None for human PSU's, we don't make mistakes :-)
        return 0

    @property
    def fault_count(self) -> int:
        """Human PSU just returns 0 for faults/error"""
        # Just say there is None for human PSU's, we don't make mistakes :-)
        return 0

    def set_output_on(self, channel: int, is_on: bool):
        """Asks the user to set an output ON or OFF"""
        on_off = "ON" if is_on else "OFF"
        print(f"Turn Channel #{channel + 1} {on_off}.")
        input("Press <Enter> when completed.")

    def close(self):
        """Does nothing for HumanPSU."""
        pass


class HumanPowerSupply(Instrument):
    """Instrument implementation for the Human PSU"""

    @classmethod
    def instrument_type(cls) -> InstrumentType:
        """Returns `InstrumentType.PowerSupply`"""
        return InstrumentType.PowerSupply

    @classmethod
    def instrument_capabilities(cls) -> Any:
        return PowerSupplyCapability()

    @classmethod
    def channel_capabilities(cls) -> List[Any]:
        return [PowerSupplyChannelCapability(0, 30, 5, None, PowerSupplyProtectionMode.OCP)]

    @contextmanager
    def use(self) -> ContextManager[Any]:
        """Yields the context object of the korad PSU."""
        human = _HumanPowerSupplyContext()
        yield human
        human.close()