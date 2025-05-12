import dataclasses
import time


@dataclasses.dataclass
class Device:
    _device_type: str
    _name: str

    def _format_measure(self, measure):
        return {
            "device_type": self._device_type,
            "name": self._name,
            "value": measure,
            "timestamp": time.time_ns()
        }

    def get_device_name(self):
        return self._name

    def get_device_type(self):
        return self._device_type

    def take_measure(self):
        pass
