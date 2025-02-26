from geopy.distance import geodesic


class Geo:

    @staticmethod
    def calculate_distance(coordinate_1, coordinate_2) -> float:
        """
        Function to Calculate distance.
        :param coordinate_1: The place Latitude.
        :param coordinate_2: The place Longitude.
        :return: Distace in KM.
        """
        dist = geodesic(coordinate_1, coordinate_2).km
        return int(dist)

    @staticmethod
    def find_nearest_capital(city_country, city_country_location_list: list):

        try:
            city_country_cords = [x for x in city_country_location_list if x[0] == city_country][0]
            city_cords = city_country_cords[1]
            city_country_location_list.remove(city_country_cords)


            # Find the nearest capital
            nearest_capital = min(
                city_country_location_list,
                key=lambda city_country_location: geodesic(city_cords, (city_country_location[1][0], city_country_location[1][1],)).km
            )
            #test =(f"{nearest_capital['city']}, {nearest_capital['country']}", (52.5200, 13.4050))

            return nearest_capital

        except Exception as e:
            return f"Error: {str(e)}"
