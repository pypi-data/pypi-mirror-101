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
from typing import ContextManager, List, Any
from contextlib import contextmanager

from .types import Multimeter, MultimeterMode, MultimeterCapability, MultimeterChannelCapability
from ..types import InstrumentType
from ..instrument import Instrument

INPUT_MAP = {
    MultimeterMode.CurrentAC: 'Measure the AC Current reading (A)',
    MultimeterMode.CurrentDC: 'Measure the DC Current reading (A)',
    MultimeterMode.Resistance: 'Measure the resistance (Ohms)',
    MultimeterMode.ResistanceFourWire: 'Measure the resistance [4-wire] (Ohms)',
    MultimeterMode.Temperature: 'Measure the temperature (C)',
    MultimeterMode.TemperatureFourWire: 'Measure the temperature [4-wire] (C)',
    MultimeterMode.VoltageDC: 'Measure the DC Voltage (V)',
    MultimeterMode.VoltageAC: 'Measure the AC Voltage (V)'
}


class _HumanDMMContext(Multimeter):
    """Human DMM (wait for user to input number)."""

    def measure(self, channel: int, mode: MultimeterMode) -> float:
        while True:
            try:
                return float(input(f"{INPUT_MAP[mode]}. Value (#.#): "))
            except ValueError:
                print("Please enter a number formatted as ##.##")

    def close(self):
        pass


class HumanDMM(Instrument):
    """Instrument context manager for the Human."""
    @classmethod
    def instrument_type(cls) -> InstrumentType:
        return InstrumentType.Multimeter

    @classmethod
    def instrument_capabilities(cls) -> Any:
        return MultimeterCapability()

    @classmethod
    def channel_capabilities(cls) -> List[Any]:
        return [MultimeterChannelCapability(6.5, 2.0, 1000, -1000,
                                            [MultimeterMode.TemperatureFourWire, MultimeterMode.Temperature,
                                             MultimeterMode.ResistanceFourWire, MultimeterMode.Resistance,
                                             MultimeterMode.CurrentDC, MultimeterMode.CurrentAC,
                                             MultimeterMode.VoltageAC, MultimeterMode.VoltageDC])]

    @contextmanager
    def use(self) -> ContextManager[Any]:
        """Creates the context variable for the Human DMM"""
        human = _HumanDMMContext()
        yield human
        human.close()
