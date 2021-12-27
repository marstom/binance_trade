from typing_extensions import Protocol


class Writeable(Protocol):
    def write(self, data):
        ...
