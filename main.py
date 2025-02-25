import random
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


def get_wikipedia_links(city_name):
    """To do. Function needs to be implemented. Now just a fake functionality,
    Here Needs to query Wiki API to get a city list from wiki page."""

    locations = CityLocations.locations
    random_locations = random.sample(locations, 10)
    # ["Berlin, Germany","Tokyo, Japan","New York City, USA"]
    return [x[0] for x in random_locations]


def calculate_distance(coord1, coord2) -> float:
    """
    Function to Calculate diastance.
    :param coord1: The place Latitude.
    :param coord2: The place Longitude.
    :return: Distace in KM.
    """
    dist = distance.geodesic(coord1, coord2).km
    return int(dist)


def calculate_cost(dist):
    """Method to calculate travel cost."""
    travel_cost = dist * 0.1  # Assume $0.1 per km travel cost
    return int(travel_cost)


def get_openai_travel_advice(location, target):
    pass


def start_game():
    """Game Loop Method."""
    print("\nWelcome to WikiSaver")
    start_location, start_cords = get_random_travel_location()
    target_location, target_cords = get_random_travel_location()

    # Ensuring Start location and End location should Not Be the same.
    while start_location == target_location:
        target_location, target_cords = get_random_travel_location()

    print(f"Starting Location: {start_location}")
    print(f"Target Destination: {target_location}")
    print("Travel wisely within budget!")

    current_location = start_location
    current_cords = start_cords
    steps = 0

    budget = None
    initial_budget = None
    while True:


        distance_to_target = calculate_distance(current_cords, target_cords)
        travel_cost = calculate_cost(distance_to_target)

        # setting budget = calculated travel_cost
        if budget is None:
            #Agssigning enough budget to user
            budget = travel_cost * 5
            initial_budget = budget

        print(f"\n******************************************")
        print(f"Current Location: {current_location}")
        print(f"Target Destination: {target_location}")
        print(f"Distance to Target: {distance_to_target} km")
        print(f"Budget Remaining: ${budget}")
        print(f"******************************************")
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


if __name__ == "__main__":
    start_game()
