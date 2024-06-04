from api import API, TreeNode
from geocoders.geocoder import Geocoder

# Перебор дерева
class SimpleTreeGeocoder(Geocoder):
    def __init__(self, samples: int | None = None, data: list[TreeNode] | None = None):
        super().__init__(samples=samples)
        if data is None:
            self.__data = API.get_areas()
        else:
            self.__data = data

    def find_path(self, nodes, area_id, path):
        for node in nodes:
            if node.id == area_id:
                path.append(node.name)
                return True
            if self.find_path(node.areas, area_id, path):
                path.append(node.name)
                return True
        return False

    def _apply_geocoding(self, area_id: str) -> str:
        """Перебираем дерево для каждого area_id и составляем полный адрес"""
        path = []
        self.find_path(self.__data, area_id, path)
        return ", ".join(reversed(path))
