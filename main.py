import json
import os
import requests
from geopy.distance import geodesic
from typing import List, Dict, Any, Optional


class GeocodingService:
    @staticmethod
    def geocode_address(address: str) -> Optional[tuple]:
        """Преобразует адрес в координаты (широта, долгота)"""
        try:
            # Используем Nominatim (OpenStreetMap) - бесплатный сервис
            url = f"https://nominatim.openstreetmap.org/search"
            params = {
                'q': address,
                'format': 'json',
                'limit': 1
            }

            headers = {
                'User-Agent': 'PriceManagerApp/1.0'
            }

            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            data = response.json()
            if data:
                return (float(data[0]['lat']), float(data[0]['lon']))

        except Exception as e:
            print(f"Ошибка геокодирования: {e}")

        return None

    @staticmethod
    def calculate_distance(coord1: tuple, coord2: tuple) -> float:
        """Рассчитывает расстояние между двумя точками в км"""
        return geodesic(coord1, coord2).km


class PriceManager:
    def __init__(self):
        self.companies_file = 'companies.json'
        self.products_file = 'products.json'
        self.user_address = "Москва, Красная площадь, 1"
        self.user_location = self._get_user_location()

    def _get_user_location(self) -> tuple:
        """Получает или запрашивает местоположение пользователя"""
        # Пробуем получить координаты из адреса
        location = GeocodingService.geocode_address(self.user_address)
        if location:
            return location

        # Если не получилось, используем координаты по умолчанию
        return (55.7558, 37.6173)  # Москва

    def load_data(self, filename: str) -> List[Dict]:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self, filename: str, data: List[Dict]):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def set_user_location(self):
        """Устанавливает местоположение пользователя по адресу"""
        print("\n=== Установка вашего местоположения ===")
        city = input("Введите ваш город: ").strip()
        street = input("Введите вашу улицу и дом: ").strip()

        user_address = f"{city}, {street}"
        location = GeocodingService.geocode_address(user_address)

        if location:
            self.user_address = user_address
            self.user_location = location
            print(f"Местоположение установлено: {user_address}")
            print(f"Координаты: {location}")
            return location
        else:
            print("Не удалось определить координаты. Используйте ручной ввод:")
            lat = float(input("Широта: "))
            lon = float(input("Долгота: "))
            self.user_location = (lat, lon)
            return (lat, lon)

    def add_company_price(self):
        print("\n=== Загрузка прайса предприятия ===")

        companies = self.load_data(self.companies_file)
        products = self.load_data(self.products_file)

        # Ввод данных о предприятии
        company_name = input("Введите название предприятия: ")
        city = input("Введите город: ").strip()
        street = input("Введите улицу и дом: ").strip()

        company_address = f"{city}, {street}"

        # Геокодирование адреса
        print("Определяем координаты...")
        location = GeocodingService.geocode_address(company_address)

        if not location:
            print("Не удалось автоматически определить координаты.")
            lat = float(input("Введите широту вручную: "))
            lon = float(input("Введите долготу вручную: "))
            location = (lat, lon)

        # Создание нового предприятия
        new_company = {
            "id": len(companies) + 1,
            "name": company_name,
            "address": company_address,
            "location": list(location)
        }
        companies.append(new_company)

        # Загрузка товаров
        print(f"\nДобавление товаров для {company_name}:")
        print("(для завершения введите 'стоп' в названии товара)")

        while True:
            product_name = input("\nНазвание товара: ").strip()
            if product_name.lower() == 'стоп':
                break

            try:
                price = float(input("Цена товара: "))

                new_product = {
                    "id": len(products) + 1,
                    "name": product_name,
                    "price": price,
                    "company_id": new_company["id"]
                }
                products.append(new_product)
                print(f"✓ Товар '{product_name}' добавлен!")

            except ValueError:
                print("❌ Ошибка! Введите корректную цену.")

        # Сохранение данных
        self.save_data(self.companies_file, companies)
        self.save_data(self.products_file, products)
        print(f"\n✅ Прайс предприятия '{company_name}' успешно загружен!")
        print(f"Адрес: {company_address}")
        print(f"Координаты: {location}")
        print(f"Добавлено товаров: {len([p for p in products if p['company_id'] == new_company['id']])}")

    def search_products(self):
        print("\n=== Поиск товаров ===")
        search_term = input("Введите название товара для поиска: ").lower().strip()

        if not search_term:
            print("Введите название товара для поиска.")
            return []

        companies = self.load_data(self.companies_file)
        products = self.load_data(self.products_file)

        # Поиск товаров
        found_products = []
        for product in products:
            if search_term in product['name'].lower():
                # Находим компанию для этого товара
                company = next((c for c in companies if c['id'] == product['company_id']), None)
                if company and 'location' in company:
                    # Рассчитываем расстояние
                    company_coords = tuple(company['location'])
                    distance = GeocodingService.calculate_distance(self.user_location, company_coords)

                    # Балльная система: цена + расстояние * коэффициент
                    distance_weight = 10  # 1 км = 10 руб "стоимости доставки"
                    total_score = product['price'] + distance * distance_weight

                    found_products.append({
                        'product': product,
                        'company': company,
                        'distance': distance,
                        'total_score': total_score
                    })

        return found_products

    def show_best_options(self, products: List[Dict]):
        if not products:
            print("❌ Товары не найдены.")
            return

        # Сортировка по общему баллу (цена + расстояние)
        sorted_products = sorted(products, key=lambda x: x['total_score'])

        print(f"\n🎯 Топ-3 лучших варианта для покупки:")
        print("=" * 70)

        for i, item in enumerate(sorted_products[:3], 1):
            product = item['product']
            company = item['company']

            print(f"{i}. 🛒 {product['name']} - {product['price']} руб.")
            print(f"   🏪 Магазин: {company['name']}")
            print(f"   📍 Адрес: {company.get('address', 'Не указан')}")
            print(f"   🚗 Расстояние: {item['distance']:.1f} км")
            print(f"   ⚖️  Общий балл (цена + расстояние): {item['total_score']:.1f}")
            print(f"   💡 Цена: {product['price']} руб. + "
                  f"Расстояние: {item['distance']:.1f} км × 10 = {item['total_score']:.1f}")
            print("-" * 50)

    def view_all_companies(self):
        companies = self.load_data(self.companies_file)
        print(f"\n🏢 Все предприятия ({len(companies)}):")
        print("=" * 50)

        for company in companies:
            if 'location' in company:
                distance = GeocodingService.calculate_distance(
                    self.user_location,
                    tuple(company['location'])
                )
            else:
                distance = "Неизвестно"

            print(f"{company['id']}. {company['name']}")
            print(f"   Адрес: {company.get('address', 'Не указан')}")
            print(f"   Расстояние от вас: {distance:.1f} км" if isinstance(distance,
                                                                           float) else f"   Расстояние: {distance}")
            print("-" * 30)

    def main_menu(self):
        while True:
            print(f"\n📍 === Система анализа прайсов ===")
            print(f"Ваше местоположение: {self.user_address}")
            print(f"Координаты: {self.user_location}")
            print("1. Загрузить прайс предприятия")
            print("2. Поиск товара")
            print("3. Изменить мое местоположение")
            print("4. Показать все предприятия")
            print("5. Выход")

            choice = input("Выберите действие: ").strip()

            if choice == '1':
                self.add_company_price()
            elif choice == '2':
                found_products = self.search_products()
                self.show_best_options(found_products)
            elif choice == '3':
                self.set_user_location()
            elif choice == '4':
                self.view_all_companies()
            elif choice == '5':
                print("👋 До свидания!")
                break
            else:
                print("❌ Неверный выбор. Попробуйте снова.")


# Запуск программы
if __name__ == "__main__":
    manager = PriceManager()

    # Создаем файлы, если они не существуют
    if not os.path.exists(manager.companies_file):
        manager.save_data(manager.companies_file, [])
    if not os.path.exists(manager.products_file):
        manager.save_data(manager.products_file, [])

    manager.main_menu()