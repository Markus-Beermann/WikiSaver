"""The CityInfo Module."""
import geonamescache


class CityInfo:
    """The CityInfo Class."""
    def __init__(self):
        self.gc = geonamescache.GeonamesCache()
        self.country_data = self.gc.get_countries()

    def fetch_data(self):
        """Fetches country and capital data from the API and stores it globally."""
        locations = []
        for country in self.country_data.values():
            country_name = country["name"]

            capital_name = country["capital"]
            if capital_name == "" or len(self.gc.get_cities_by_name(capital_name)) == 0:
                continue

            city_info = self.gc.get_cities_by_name(capital_name)
            if len(city_info) == 0:
                continue

            key = list(city_info[0].keys())[0]
            latitude = city_info[0][key]["latitude"]
            longitude = city_info[0][key]["longitude"]
            locations.append((f"{capital_name}, {country_name}", (latitude, longitude)))

        return locations
