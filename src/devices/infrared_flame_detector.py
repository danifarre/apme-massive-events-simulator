import dataclasses

from devices.device import Device


@dataclasses.dataclass
class InfraredFlameDetector(Device):

    def __init__(self, name):
        super().__init__("infrared_flame_detector", name)

    def take_measure(self):
        return self._format_measure(0)
