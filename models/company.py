from typing import Dict, List

class Company:
    def __init__(self, id: int, name: str, address: str, location: List[float]):
        self.id = id
        self.name = name
        self.address = address
        self.location = location

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "location": self.location
        }
