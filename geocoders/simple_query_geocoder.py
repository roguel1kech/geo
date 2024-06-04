from geocoders.geocoder import Geocoder
from api import API

# Алгоритм "в лоб"
class SimpleQueryGeocoder(Geocoder):
    def _apply_geocoding(self, area_id: str) -> str:
        """Для каждого area_id делаем запросы к API и формируем полный адрес"""
        address_parts = []
        while area_id:
            area = API.get_area(area_id)
            address_parts.append(area.name)
            area_id = area.parent_id
        return ", ".join(reversed(address_parts))
