import time

from api import API
from geocoders.geocoder import Geocoder
from geocoders.memorized_tree_geocoder import MemorizedTreeGeocoder
from geocoders.simple_query_geocoder import SimpleQueryGeocoder
from geocoders.simple_tree_geocoder import SimpleTreeGeocoder

def format_time(start_ns: int, end_ns: int) -> str:
    diff = end_ns - start_ns

    diff_ms = diff / 10**6
    if diff_ms > 1000:
        seconds = round(diff_ms / 1000, 2)
        return f"{seconds} s"
    else:
        mills = round(diff_ms, 2)
        return f"{mills} ms"

def main():
    areas_data = API.get_areas()

    geocoder_list: list[Geocoder] = [
        SimpleQueryGeocoder(samples=10),
        SimpleTreeGeocoder(samples=10, data=areas_data),
        MemorizedTreeGeocoder(samples=10, data=areas_data),
        SimpleTreeGeocoder(samples=1000, data=areas_data),
        MemorizedTreeGeocoder(samples=1000, data=areas_data),
        SimpleTreeGeocoder(samples=10000, data=areas_data),
        MemorizedTreeGeocoder(samples=10000, data=areas_data),
        MemorizedTreeGeocoder(data=areas_data),
    ]

    for geocoder in geocoder_list:
        class_name = geocoder.__class__.__name__
        samples_num = geocoder.__dict__.get("_samples")
        if samples_num is None:
            samples_num = len(areas_data)

        start_time_ns = time.time_ns()
        for area_id in range(samples_num):  # Геокодируем каждый area_id
            geocoder._apply_geocoding(str(area_id))
        end_time_ns = time.time_ns()

        time_formatted = format_time(start_time_ns, end_time_ns)

        print(f"{class_name} [{samples_num}]: {time_formatted}")

if __name__ == "__main__":
    main()
