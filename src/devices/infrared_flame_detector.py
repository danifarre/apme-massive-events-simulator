import dataclasses

from devices.device import Device


@dataclasses.dataclass
class InfraredFlameDetector(Device):

    def __init__(self, name):
        super().__init__("infrared_flame_detector", name)

    def take_measure(self, measurement=0):
        return self._format_measure(measurement)
