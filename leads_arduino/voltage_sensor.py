from typing import override as _override

from leads import Device as _Device


class VoltageSensor(_Device):
    def __init__(self) -> None:
        super().__init__()
        self._voltage: float = 0

    @_override
    def update(self, data: float) -> None:
        self._voltage = data

    @_override
    def read(self) -> float:
        return self._voltage
