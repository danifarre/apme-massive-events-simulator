import dataclasses

from devices.device import Device
import random


@dataclasses.dataclass
class Anemometer(Device):

    def __init__(self, name):
        super().__init__("anemometer", name)

    def take_measure(self):
        measure = float(random.uniform(10.0, 12.0))
        return self._format_measure(measure)
