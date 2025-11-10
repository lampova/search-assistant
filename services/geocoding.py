import requests
from geopy.distance import geodesic
from typing import Optional, Tuple

class GeocodingService:
    @staticmethod
    def geocode_address(address: str) -> Optional[Tuple[float, float]]:
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {'q': address, 'format': 'json', 'limit': 1}
            headers = {'User-Agent': 'PriceManagerApp/1.0'}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data:
                return (float(data[0]['lat']), float(data[0]['lon']))
        except Exception as e:
            print(f"Ошибка геокодирования: {e}")
        return None

    @staticmethod
    def calculate_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        return geodesic(coord1, coord2).km
