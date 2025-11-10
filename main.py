import os
from document import Document
from geopy import location
import json

from conf import client
from gpt import smart_product_search
from models.company import Company
from models.product import Product
from models.user import User
from services.geocoding import GeocodingService
from services.file_parser import FileParser
from utils.data_storage import DataStorage
from typing import List, Dict

class PriceManager:
    def __init__(self):
        self.companies_file = 'companies.json'
        self.products_file = 'products.json'
        self.user = User("Москва, Красная площадь, 1", GeocodingService.geocode_address("Москва, Красная площадь, 1") or (55.7558, 37.6173))

    def add_company_from_file(self, company_name: str, file_path: str, address: str = None) -> str:
        companies = DataStorage.load_data(self.companies_file)
        products = DataStorage.load_data(self.products_file)

        if address:
            location = GeocodingService.geocode_address(address)
            if not location:
                return f"❌ Не удалось определить координаты для адреса: {address}"
        else:
            address = "Адрес не указан"
            location = [55.7558, 37.6173]

        new_company = Company(len(companies) + 1, company_name, address, list(location))
        companies.append(new_company.to_dict())

        # Теперь вызываем новый парсер
        try:
            parsed_products = FileParser.parse_excel_file(file_path)
        except Exception as e:
            return f"❌ Ошибка обработки файла: {str(e)}"

        if not parsed_products:
            return "❌ В файле не найдено товаров с ценами"

        added_count = 0
        for product_data in parsed_products:
            new_product = Product(len(products) + 1, product_data["name"], product_data["price"], new_company.id)
            products.append(new_product.to_dict())
            added_count += 1

        DataStorage.save_data(self.companies_file, companies)
        DataStorage.save_data(self.products_file, products)

        return (f"✅ Предприятие '{company_name}' добавлено успешно!\n"
                f"📁 Файл: {os.path.basename(file_path)}\n"
                f"📊 Обработано товаров: {len(parsed_products)}\n"
                f"✅ Добавлено товаров: {added_count}\n"
                f"📍 Адрес: {address}")

    import json

    def search_products(self, search_term: str, distance_weight: float = 10) -> list:
        companies = DataStorage.load_data(self.companies_file)
        products = DataStorage.load_data(self.products_file)
        found_products = []

        for product in products:
            company = next((c for c in companies if c['id'] == product['company_id']), None)
            if company and 'location' in company:
                company_coords = tuple(company['location'])
                distance = GeocodingService.calculate_distance(self.user.location, company_coords)
                total_score = product['price'] + distance * distance_weight

                found_products.append({
                    'product': product,
                    'company': company,
                    'distance': distance,
                    'total_score': total_score
                })

        if not found_products:
            return []

        llm_results = smart_product_search(found_products, search_term)
        product_map = {(fp['product']['name'], fp['company']['name']): fp for fp in found_products}

        final_results = []
        for item in llm_results:
            key = (item['name'], item['company'])
            if key in product_map:
                item['total_score'] = product_map[key]['total_score']
                final_results.append(item)

        final_results_sorted = sorted(final_results, key=lambda x: x['total_score'])

        return final_results_sorted

    def get_all_companies(self) -> List[Dict]:
        companies = DataStorage.load_data(self.companies_file)
        result = []
        for company in companies:
            if 'location' in company:
                distance = GeocodingService.calculate_distance(self.user.location, tuple(company['location']))
            else:
                distance = "Неизвестно"
            result.append({
                'id': company['id'],
                'name': company['name'],
                'address': company.get('address', 'Не указан'),
                'distance': distance
            })
        return result

    def validate_price_file(self, file_path: str) -> bool:
        if not file_path.lower().endswith('.docx'):
            return False
        if not os.path.exists(file_path):
            return False
        try:
            doc = Document(file_path)
            return len(doc.paragraphs) > 0
        except:
            return False

    def get_file_stats(self, file_path: str) -> Dict:
        try:
            products = FileParser.parse_docx_file(file_path)
            return {
                'total_lines': len([p for p in Document(file_path).paragraphs if p.text.strip()]),
                'valid_products': len(products),
                'avg_price': sum(p['price'] for p in products) / len(products) if products else 0
            }
        except:
            return {'total_lines': 0, 'valid_products': 0, 'avg_price': 0}

    def get_user_location_info(self) -> str:
        return f"{self.user.address}\nКоординаты: {self.user.location}"

    def set_user_location(self, city: str, street: str) -> bool:
        user_address = f"{city}, {street}"
        location = GeocodingService.geocode_address(user_address)
        if location:
            self.user.address = user_address
            self.user.location = location
            return True
        return False




