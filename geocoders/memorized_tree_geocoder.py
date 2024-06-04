from api import TreeNode, API
from geocoders.geocoder import Geocoder

# Инверсия дерева
class MemorizedTreeGeocoder(Geocoder):
    def __init__(self, samples: int | None = None, data: list[TreeNode] | None = None):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data
        self.memo = {}
        self.build_memo(self.__data, [])

    def build_memo(self, nodes, path):
        for node in nodes:
            path.append(node.name)
            self.memo[node.id] = ", ".join(path)
            self.build_memo(node.areas, path)
            path.pop()

    def _apply_geocoding(self, area_id: str) -> str:
        """Возвращаем данные из словаря с адресами"""
        return self.memo.get(area_id, "Unknown area")
