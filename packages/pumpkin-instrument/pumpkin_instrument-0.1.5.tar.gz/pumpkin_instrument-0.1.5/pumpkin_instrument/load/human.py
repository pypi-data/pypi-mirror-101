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

from contextlib import contextmanager
from typing import ContextManager, List, Any
from datetime import timedelta


from .types import Load, LoadMode, LoadCapability, LoadChannelCapability
from ..types import InstrumentType
from ..instrument import Instrument

STATE_MAP = {
    LoadMode.Current: "Place the Load into Constant Current mode",
    LoadMode.Power: "Place the Load into Constant Power mode",
    LoadMode.Resistance: "Place the Load into Constant Resistance mode",
    LoadMode.Voltage: "Place the Load into Constant Voltage mode",
}
UNITS_MAP = {
    LoadMode.Current: "Amps",
    LoadMode.Power: "Watts",
    LoadMode.Resistance: "Ohms",
    LoadMode.Voltage: "Volts",
}


class _HumanLoadContext(Load):
    """The Human Load context."""

    def set_output_on(self, channel: int, is_on: bool):
        """Asks the user to turn the load ON or OFF."""
        on_off = "ON" if is_on else "OFF"
        input(f"Please turn {on_off} {channel + 1} of the Load. Press <Enter> when completed.")

    def set_output_state(self, channel: int, mode: LoadMode, value: float):
        """Asks the user to set the load into the specified output state."""
        print(STATE_MAP[mode])
        print(f"Set the Load for {value:.3f} {UNITS_MAP[mode]}")
        input("Press <Enter> when done ...")

    def get_load_voltage(self, channel: int) -> float:
        """Asks the user for the voltage displayed on the load."""
        while True:
            try:
                return float(input("Please enter the Voltage displayed on the Load (V): "))
            except ValueError:
                # Keep going til they give us good stuff
                pass

    def get_load_current(self, channel: int) -> float:
        """Asks the user for the current displayed on the load."""
        while True:
            try:
                return float(input("Please enter the Current displayed on the Load (A): "))
            except ValueError:
                # Keep going til they give us good stuff
                pass

    def get_load_power(self, channel: int) -> float:
        """Asks the user for the power displayed on the load."""
        while True:
            try:
                return float(input("Please enter the Power displayed on the Load (W): "))
            except ValueError:
                # Keep going til they give us good stuff
                pass

    def get_load_resistance(self, channel: int) -> float:
        """Asks user for the resistance displayed on the load"""
        while True:
            try:
                return float(input("Please enter the Resistance displayed on the Load (V): "))
            except ValueError:
                # Keep going til they give us good stuff
                pass

    def get_load_discharge_time(self, channel: int) -> timedelta:
        """Queries the load for the total discharge time."""
        raise NotImplementedError()

    def get_load_watthours(self, channel: int) -> float:
        """Queries the load for the total watthour discharge time."""
        raise NotImplementedError()

    def get_load_capacity(self, channel: int) -> float:
        """Queries the load for the mA capacity of the battery."""
        raise NotImplementedError()

    def close(self):
        """Does nothing for the Human Load"""
        pass


class HumanLoad(Instrument):
    @classmethod
    def instrument_capabilities(cls) -> Any:
        return LoadCapability()

    @classmethod
    def channel_capabilities(cls) -> List[Any]:
        """
        TekPower 3710A is a single-channel load with CC/CR/CP modes.
        """
        return [LoadChannelCapability(max_voltage=360.0,
                                      min_voltage=0.0,
                                      max_power=150.0,
                                      modes=[
                                          LoadMode.Resistance,
                                          LoadMode.Power,
                                          LoadMode.Current
                                      ])]

    @classmethod
    def instrument_type(cls) -> InstrumentType:
        return InstrumentType.Load

    @contextmanager
    def use(self) -> ContextManager[Any]:
        """
        Returns the instance of the human load
        """
        human = _HumanLoadContext()
        yield human
        human.close()
