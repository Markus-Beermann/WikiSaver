"""The WikiSaver Main Module."""
import random

from capitals_and_countries import CapitalAndCountries
from city_info import CityInfo
from gemini_ai_helper import GeminiAIHelper
from geo import Geo
from print_helpers import PrintHelper
from wiki import Wiki

AI_HINT_DICT = {
    1: {"desc": "Continent of the Target city (cost - 5% of initial budget).",
          "query": "Give me the name of the continent for the city {key1} in country {key2}.",
          "cost_method": lambda x: x * 0.05},
    2: {"desc": "Continent of the Target city + Language (cost - 10% of initial budget).",
          "query": "Give me the name of the continent for the city {key1} in country {key2} and the main language spoken.",
          "cost_method": lambda x: x * 0.1},
    3: {"desc": "Show 3 Countries bordering the target country (cost - 15% of initial budget).",
          "query": "Give me at least 3 countries bordering the country in which city {key1} in country {key2} is located.",
          "cost_method": lambda x: x * 0.15},
}


def get_random_travel_location(locations: list):
    return random.choice(locations)


def get_travel_location_coordinates(city_name: str, locations: list):
    """Function to get the given location coordinates."""
    city_dict = dict(x for x in locations if x[0].lower() == city_name.lower())
    # return city_dict[city_name]
    return list(city_dict.values())[0]


def calculate_cost(dist):
    """Method to calculate travel cost."""
    travel_cost = dist * 0.1  # Assume $0.1 per km travel cost
    return int(travel_cost)


def get_capital_country_wiki_results(current_location, country_data):
    """Wrapper method for wiki page capital country list"""

    wikipedia_page = get_wikipedia_page(current_location, country_data)
    links = CapitalAndCountries.get_capitals_and_countries_from_wikipedia_page(current_location,
                                                                               country_data, wikipedia_page)
    lower_links = [x.lower() for x in links]
    for i,lower_link in enumerate(lower_links):
        if current_location.lower() == lower_link:
            links.pop(i)
            break

    if len(links) == 0:
        links = get_capital_country_wiki_results_fail_safe(current_location, country_data)

    return links

def get_wikipedia_page(current_location, country_data):
    while True:
        wikipedia_page = Wiki.get_wikipedia_page_text(current_location)
        if wikipedia_page is not None:
            return wikipedia_page
        else:
            current_location_tuple = Geo.find_nearest_capital(current_location, country_data)
            current_location = current_location_tuple[0]

def get_capital_country_wiki_results_fail_safe(current_location, country_data):
    while True:
        current_location_tuple = Geo.find_nearest_capital(current_location, country_data)
        current_location = current_location_tuple[0]
        wikipedia_page = Wiki.get_wikipedia_page_text(current_location)
        links = CapitalAndCountries.get_capitals_and_countries_from_wikipedia_page(current_location,
                                                                                   country_data, wikipedia_page)
        lower_links = [x.lower() for x in links]
        for i, lower_link in enumerate(lower_links):
            if current_location.lower() == lower_link:
                links.pop(i)
                break

        if len(links) > 0:
            break
    return links

def get_all_location_cost(start_coordinates, all_links, country_data):
    """Get the cost for all given links."""
    travel_cost_dict = {}
    for link in all_links:
        link_cords = get_travel_location_coordinates(link, country_data)
        # Calculate distance to target
        distance_to_target = Geo.calculate_distance(start_coordinates, link_cords)
        # Calculate travel cost
        travel_cost = calculate_cost(distance_to_target)
        travel_cost_dict[link] = travel_cost
    return travel_cost_dict

def loose_condition(travel_cost_dict: dict ,budget):
    """Method to evaluate loose condition"""
    cost_list = travel_cost_dict.values()
    return all(budget < x for x in cost_list)


def start_game():
    """Game Loop Method."""
    PrintHelper.print_welcome_msg()

    city_info = CityInfo()
    country_data = city_info.fetch_data()

    # Get Random Start and End Locations.
    start_location, start_cords = get_random_travel_location(country_data)
    target_location, target_cords = get_random_travel_location(country_data)
    # open_ai = OpenAIHelper()
    # open_ai.active = False

    # Ensuring Start location and End location should Not Be the same.
    while start_location == target_location:
        target_location, target_cords = get_random_travel_location(country_data)

    PrintHelper.pr_menu_headers(f"Starting Location: {start_location}")
    PrintHelper.pr_menu_headers(f"Target Destination: {target_location}")
    PrintHelper.pr_menu("Travel wisely within budget!")

    # Initialize Budget, Locations and steps
    current_location = start_location
    current_cords = start_cords
    steps = 0

    budget = None
    initial_budget = None

    gemini_ai = GeminiAIHelper()

    while True:  # current_location !=target_location
        # Calculate distance to target
        distance_to_target = Geo.calculate_distance(current_cords, target_cords)
        # Calculate travel cost
        travel_cost = calculate_cost(distance_to_target)

        # setting budget = calculated travel_cost
        if budget is None:
            # Assigning enough budget to user
            budget = travel_cost * 5
            initial_budget = budget

        print("\n")
        PrintHelper.print_seperator()
        PrintHelper.pr_menu_headers(f"Current Location: {current_location}")
        PrintHelper.pr_menu_headers(f"Target Destination: {target_location}")
        PrintHelper.pr_menu_headers(f"Distance to Target: {distance_to_target} km")
        PrintHelper.pr_menu_headers(f"Budget Remaining: ${budget}")
        PrintHelper.print_seperator()
        links = get_capital_country_wiki_results(current_location, country_data)
        travel_cost_dict = get_all_location_cost(current_cords, links, country_data)

        if loose_condition(travel_cost_dict , budget):
            print("\n")
            PrintHelper.print_loser()
            PrintHelper.pr_error("You lost the game.")
            PrintHelper.pr_menu_option_1(f"But look on the bright side, {current_location} is nice to settle down.")
            if gemini_ai.active:
                PrintHelper.pr_menu_option_1(f"Why {current_location}?")
                result = gemini_ai.get_gemini_query_result(f"Give me interesting facts about {current_location}.")
                PrintHelper.pr_menu(result)
            PrintHelper.pr_menu_option_1(f"As You lost the game.Happy Living in {current_location}")
            break

        # Block to get the User Choice.
        while True:
            try:
                PrintHelper.pr_menu_headers("\nAvailable Travel Links Choose a WIKI link by index (1,2,3....):")
                for i, link in enumerate(links, start=1):  # Show all links
                    if travel_cost_dict[link] > budget:
                        PrintHelper.pr_menu_option_2(f"{i}. {link}", f"cost:${travel_cost_dict[link]}")
                    else:
                        PrintHelper.pr_menu(f"{i}. {link} cost:${travel_cost_dict[link]}")

                ai_text = "[00 for AI hint.]" if gemini_ai.active else ""
                choice = PrintHelper.pr_input(
                    f"Enter choice 1 to {len(links)} or {ai_text} [0 to quit.] ").strip()

                if gemini_ai.active and choice == "00":
                    budget = game_ai(gemini_ai, target_location, initial_budget=initial_budget, budget=budget)
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

        if current_location.lower() == target_location.lower():
            PrintHelper.print_winner()
            PrintHelper.pr_menu(f"\nCongratulations! You reached {target_location}")
            PrintHelper.pr_menu(f"You spent just: ${initial_budget - budget}")
            PrintHelper.pr_menu(f"You reached {target_location} in {steps} steps.")
            break



def game_ai(gemini_ai, target, initial_budget, budget):
    """Method for Game AI."""
    print("\n")
    PrintHelper.pr_menu_headers("***********Welcome I am Globetrotters AI model gemini-2.0-flash.***********")
    PrintHelper.pr_menu("Hmm How can i help? , Please choose one option.")
    print("\n")
    while True:
        for k, v in AI_HINT_DICT.items():
            PrintHelper.pr_menu(f"{k}. {v['desc']} Cost: ${v['cost_method'](initial_budget)}")

        selected_ai_hint = None
        while True:
            try:
                ai_choice = int(PrintHelper.pr_input(
                    f"Enter choice for AI hint or 0 to Exit:").strip())

                if ai_choice == 0:
                    break
                if not 1 <= ai_choice <= len(AI_HINT_DICT):
                    raise ValueError

                selected_ai_hint = AI_HINT_DICT[ai_choice]
                cost = selected_ai_hint["cost_method"](initial_budget)
                if cost > budget:
                    PrintHelper.pr_error(f"You just have ${budget} and for AI hint ${cost} is required.")
                    continue

                break
            except ValueError:
                PrintHelper.pr_error(f"Please enter valid number from 1 to {len(AI_HINT_DICT)}")
        if ai_choice == 0:
            break
        if selected_ai_hint is not None:
            city = target.split(",")[0].strip()
            country = target.split(",")[1].strip()
            query = selected_ai_hint["query"].format(key1=city,key2=country)
            result = gemini_ai.get_gemini_query_result(query)
            PrintHelper.pr_bold(result)
            cost = selected_ai_hint["cost_method"](initial_budget)
            budget = budget - cost
            PrintHelper.pr_menu_headers(f"Your remaining Budget is ${budget}.")

    return budget


if __name__ == "__main__":
    start_game()
