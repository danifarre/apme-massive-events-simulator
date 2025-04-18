import dataclasses

from devices.device import Device
import random


@dataclasses.dataclass
class Thermometer(Device):

    def __init__(self, name):
        super().__init__("thermometer", name)

    def take_measure(self):
        measure = float(random.uniform(24.0, 26.0))
        return self._format_measure(measure)
