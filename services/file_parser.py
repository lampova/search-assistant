# services/file_parser.py
import openpyxl
from typing import List, Dict

class FileParser:
    @staticmethod
    def parse_excel_file(file_path: str) -> List[Dict]:
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active

        products = []
        # Предполагаем: первая колонка — название, вторая — цена
        # Пропускаем заголовки
        rows = list(ws.iter_rows(values_only=True))
        for row in rows[1:]:
            if row and len(row) >= 2:
                name = str(row[0]).strip()
                try:
                    price = float(str(row[1]).replace(',', '.'))
                except (TypeError, ValueError):
                    continue
                if name and price:
                    products.append({
                        'name': name,
                        'price': price
                    })
        return products
