import dataclasses

from devices.device import Device


@dataclasses.dataclass
class SmokeDetector(Device):

    def __init__(self, name):
        super().__init__("smoke_detector", name)

    def take_measure(self):
        return self._format_measure(0)
