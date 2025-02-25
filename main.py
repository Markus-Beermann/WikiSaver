"""The WikiSaver Main Module."""
import random
import re

from geopy import distance
from city_locations import CityLocations


def get_random_travel_location():
    locations = CityLocations.locations
    return random.choice(locations)


def get_travel_location_coordinates(city_name):
    """Function to get the given location coordinates."""
    locations = CityLocations.locations
    city_dict = dict(x for x in locations if x[0] == city_name)
    return city_dict[city_name]


def get_wikipedia_links(city_name) -> list:
    """To do. Function needs to be implemented. Now just a fake functionality,
    Here Needs to query Wiki API to get a city list from wiki page.
    To do. Function Features:
    1. Query wiki API to get the page with city_name.
    2. Search all the cities on the wiki page.
    3. Create a list like ["Berlin, Germany", "Tokyo, Japan", "New York City, USA"]
     """

    locations = CityLocations.locations
    random_locations = random.sample(locations, 10)
    # ["Berlin, Germany","Tokyo, Japan","New York City, USA"]
    return [x[0] for x in random_locations]


def get_capitals_from_wikipedia_page(wikipedia_page):
    """finds capitals on the wikipedia page and returns them in a list together with their country"""
    locations = CityLocations.locations
    # ["Berlin, Germany","Tokyo, Japan","New York City, USA"]
    capitals_countries_list = [capital_country_pair[0] for capital_country_pair in locations]

    capitals_list = [capital_country_pair.split(",")[0] for capital_country_pair in capitals_countries_list]
    found_capitals_list = []
    #replacing unwanted characters
    wikipedia_page = re.sub("[<>,}.;/{=!?']", " ", wikipedia_page)
    #appending found capitals to our list if they are surrounded by whitespace
    found_capitals_list = [capital for capital in capitals_list if re.search('(^|\s)' + capital + '($|\s)', wikipedia_page)]

    found_capitals_cities_list = [
        capital_country
        for capital_country in capitals_countries_list
        if capital_country.split(",")[0] in set(found_capitals_list)]

    #loop through capitals list and for every capital check whether it is in the capital_country_pair of our capitals_countries_list
    #found_capitals_cities_list = []
    #for capital in found_capitals_list:
    #    for capital_country in capitals_countries_list:
    #        if capital in capital_country:
    #            found_capitals_cities_list.append(capital_country)

    return found_capitals_cities_list




def calculate_distance(coord1, coord2) -> float:
    """
    Function to Calculate distance.
    :param coord1: The place Latitude.
    :param coord2: The place Longitude
    :return: Distance in KM.
    """
    dist = distance.geodesic(coord1, coord2).km
    return int(dist)


def calculate_cost(dist):
    """Method to calculate travel cost."""
    travel_cost = dist * 0.1  # Assume $0.1 per km travel cost
    return int(travel_cost)


def get_openai_travel_advice(location, target):
    """How we can use openAI for wikiSaver???. Ideas"""
    pass


def start_game():
    print(get_wikipedia_links("Tokyo"))
    """Game Loop Method."""
    print("\nWelcome to WikiSaver")
    #Get Random Start and End Locations.
    start_location, start_cords = get_random_travel_location()
    target_location, target_cords = get_random_travel_location()

    # Ensuring Start location and End location should Not Be the same.
    while start_location == target_location:
        target_location, target_cords = get_random_travel_location()


    print(f"Starting Location: {start_location}")
    print(f"Target Destination: {target_location}")
    print("Travel wisely within budget!")

    #Initialize Budget, Locations and steps
    current_location = start_location
    current_cords = start_cords
    steps = 0

    budget = None
    initial_budget = None



    while True:#current_location !=target_location

        #Calculate distance to target
        distance_to_target = calculate_distance(current_cords, target_cords)
        #Calculate travel cost
        travel_cost = calculate_cost(distance_to_target)

        # setting budget = calculated travel_cost
        if budget is None:
            #Agssigning enough budget to user
            budget = travel_cost * 5
            initial_budget = budget

        print("\n******************************************")
        print(f"Current Location: {current_location}")
        print(f"Target Destination: {target_location}")
        print(f"Distance to Target: {distance_to_target} km")
        print(f"Budget Remaining: ${budget}")
        print("******************************************")
        links = get_wikipedia_links(current_location)
        # Block to get the User Choice.
        while True:
            try:
                print("\nAvailable Travel Links Choose a WIKI link by index (1,2,3....):")
                for i, link in enumerate(links, start=1):  # Show only 10 travel-related links
                    print(f"{i}. {link}")
                choice = input("Enter choice or [empty text for more choices / 0 to quit.] ").strip()
                if choice == "":
                    links = get_wikipedia_links(current_location)
                    continue  # empty text for more choices
                if choice == "0":
                    break  # 0 to quit

                choice = int(choice)
                if not 1 <= choice <= 10:
                    raise ValueError
                break
            except ValueError:
                print("Please enter valid choice a number from 1 to 10")
        if choice == "0":
            break # 0 to quit

        next_location = links[choice - 1]
        # Now calculate the travel cost
        # Get current location coordinates
        next_loc_cords = get_travel_location_coordinates(next_location)
        distance_to_choice = calculate_distance(current_cords, next_loc_cords)
        travel_cost = calculate_cost(distance_to_choice)

        if budget - travel_cost <= 0:
            print("Not enough budget! Choose a closer destination.")
            continue

        budget -= travel_cost

        # Now user has reached next location
        current_location = next_location
        current_cords = next_loc_cords
        steps += 1

        if current_location == target_location:
            print(f"\nCongratulations! You reached {target_location}")
            print(f"You spent just: ${initial_budget - budget}")
            print(f"You reached {target_location} in {steps} steps.")
            break


def main():
    print(get_capitals_from_wikipedia_page("Hallo23<<Tokyo//, Berlin"))


if __name__ == "__main__":
    #start_game()
    main()
