from typing import Tuple

class User:
    def __init__(self, address: str, location: Tuple[float, float]):
        self.address = address
        self.location = location

    def set_location(self, address: str, location: Tuple[float, float]):
        self.address = address
        self.location = location
