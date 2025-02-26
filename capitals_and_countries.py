import re


class CapitalAndCountries:
    @staticmethod
    def get_capitals_and_countries_from_wikipedia_page(current_location, locations, wikipedia_page):
        """finds capitals on the wikipedia page and returns them in a list together with their country"""
        # ["Berlin, Germany","Tokyo, Japan","New York City, USA"]
        capitals_countries_list = [capital_country_pair[0].lower() for capital_country_pair in locations]

        capitals_list = [capital_country_pair.split(",")[0].strip() for capital_country_pair in capitals_countries_list]
        countries_list = [capital_country_pair.split(",")[1].strip() for capital_country_pair in capitals_countries_list]

        # replacing unwanted characters
        wikipedia_page = re.sub(r"[<>,}.;/{=!?']", " ", wikipedia_page.lower())
        # appending found capitals/countries to our list if they are surrounded by whitespace
        found_capitals_list = [capital for capital in capitals_list if
                               re.search(r'(^|\s)' + capital + r'($|\s)', wikipedia_page)]

        found_countries_list = [country for country in countries_list if
                                re.search(r'(^|\s)' + country + r'($|\s)', wikipedia_page)]

        found_capitals_countries_list = [
            capital_country.title()
            for capital_country in capitals_countries_list
            if capital_country.split(",")[0].strip() in set(found_capitals_list)
            or capital_country.split(",")[1].strip() in set(found_countries_list)]

        return found_capitals_countries_list
