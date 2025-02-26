"""The WikiSaver Main Module."""
import random

from capitals_and_countries import CapitalAndCountries
from city_info import CityInfo
from gemini_ai_helper import GeminiAIHelper
from geo import Geo
from open_ai_helper import OpenAIHelper
from print_helpers import PrintHelper
from wiki import Wiki


def get_random_travel_location(locations: list):
    return random.choice(locations)


def get_travel_location_coordinates(city_name: str, locations: list):
    """Function to get the given location coordinates."""
    city_dict = dict(x for x in locations if x[0].lower() == city_name.lower())

    #return city_dict[city_name]
    return list(city_dict.values())[0]


def calculate_cost(dist):
    """Method to calculate travel cost."""
    travel_cost = dist * 0.1  # Assume $0.1 per km travel cost
    return int(travel_cost)


def get_capital_country_wiki_results(current_location, country_data):
    """Wrapper method for wiki page capital country list"""

    wikipedia_page = Wiki.get_wikipedia_page_text(current_location)
    links = CapitalAndCountries.get_capitals_and_countries_from_wikipedia_page(current_location,
                                                                               country_data, wikipedia_page)
    if current_location in links:  # Remove the current location from wiki results
        links.remove(current_location)

    if len(links) == 0:
        while True:
            current_location_tuple = Geo.find_nearest_capital(current_location, country_data)
            current_location = current_location_tuple[0]
            wikipedia_page = Wiki.get_wikipedia_page_text(current_location)
            links = CapitalAndCountries.get_capitals_and_countries_from_wikipedia_page(current_location,
                                                                                       country_data, wikipedia_page)
            if current_location in links:  # Remove the current location from wiki results
                links.remove(current_location)
            if len(links) > 0:
                break

    return links


def get_openai_travel_advice(location, target):
    """How we can use openAI for wikiSaver???. Ideas"""
    pass


def start_game():
    """Game Loop Method."""
    PrintHelper.print_welcome_msg()

    city_info = CityInfo()
    country_data = city_info.fetch_data()

    # Get Random Start and End Locations.
    start_location, start_cords = get_random_travel_location(country_data)

    # test
    #start_location = "Yamoussoukro, Ivory Coast"
    #start_location = "Fort-De-France, Martinique"
    #start_location = "Sarajevo, Bosnia And Herzegovina"
    #start_cords = get_travel_location_coordinates(start_location, country_data)

    # test ends

    target_location, target_cords = get_random_travel_location(country_data)
    # open_ai = OpenAIHelper()
    # open_ai.active = False
    # gemini_ai = GeminiAIHelper()
    # if gemini_ai.active:
    #     test = gemini_ai.get_wikipedia_links(target_location)

    # Ensuring Start location and End location should Not Be the same.
    while start_location == target_location:
        target_location, target_cords = get_random_travel_location(country_data)

    PrintHelper.pr_menu(f"Starting Location: {start_location}")
    PrintHelper.pr_menu(f"Target Destination: {target_location}")
    PrintHelper.pr_menu("Travel wisely within budget!")

    # Initialize Budget, Locations and steps
    current_location = start_location
    current_cords = start_cords
    steps = 0

    budget = None
    initial_budget = None

    while True:  # current_location !=target_location
        # Calculate distance to target
        distance_to_target = Geo.calculate_distance(current_cords, target_cords)
        # Calculate travel cost
        travel_cost = calculate_cost(distance_to_target)

        # setting budget = calculated travel_cost
        if budget is None:
            # Assigning enough budget to user
            budget = travel_cost * 10
            initial_budget = budget

        print("\n")
        PrintHelper.print_seperator()
        PrintHelper.pr_menu(f"Current Location: {current_location}")
        PrintHelper.pr_menu(f"Target Destination: {target_location}")
        PrintHelper.pr_menu(f"Distance to Target: {distance_to_target} km")
        PrintHelper.pr_menu(f"Budget Remaining: ${budget}")
        PrintHelper.print_seperator()
        links = get_capital_country_wiki_results(current_location, country_data)
        # Block to get the User Choice.
        while True:
            try:
                PrintHelper.pr_menu("\nAvailable Travel Links Choose a WIKI link by index (1,2,3....):")
                for i, link in enumerate(links, start=1):  # Show all links
                    PrintHelper.pr_menu(f"{i}. {link}")
                choice = PrintHelper.pr_input(f"Enter choice 1 to {len(links)} or [00 for AI hint.] [0 to quit.] ").strip()
                if choice == "00":
                    PrintHelper.pr_bold("AI hint coming soon.")
                    continue

                if choice == "0":
                    break  # 0 to quit

                choice = int(choice)
                if not 1 <= choice <= len(links):
                    raise ValueError
                break
            except ValueError:
                PrintHelper.pr_error(f"Please enter valid choice a number from 1 to {len(links)}")
        if choice == "0":
            break  # 0 to quit

        next_location = links[choice - 1]
        # Now calculate the travel cost
        # Get current location coordinates
        next_loc_cords = get_travel_location_coordinates(next_location, country_data)
        distance_to_choice = Geo.calculate_distance(current_cords, next_loc_cords)
        travel_cost = calculate_cost(distance_to_choice)

        if budget - travel_cost <= 0:
            PrintHelper.pr_error("Not enough budget! Choose a closer destination.")
            continue

        budget -= travel_cost

        # Now user has reached next location
        current_location = next_location
        current_cords = next_loc_cords
        steps += 1

        if current_location == target_location:
            PrintHelper.pr_menu(f"\nCongratulations! You reached {target_location}")
            PrintHelper.pr_menu(f"You spent just: ${initial_budget - budget}")
            PrintHelper.pr_menu(f"You reached {target_location} in {steps} steps.")
            break


if __name__ == "__main__":
    start_game()
