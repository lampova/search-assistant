import json
import os
from typing import List, Dict

class DataStorage:
    @staticmethod
    def load_data(filename: str) -> List[Dict]:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    @staticmethod
    def save_data(filename: str, data: List[Dict]):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
