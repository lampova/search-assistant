from typing import Dict

class Product:
    def __init__(self, id: int, name: str, price: float, company_id: int):
        self.id = id
        self.name = name
        self.price = price
        self.company_id = company_id

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "company_id": self.company_id
        }
