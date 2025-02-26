"""Module for wikipedia operations."""
from wikipedia import wikipedia, exceptions


class Wiki:
    """Class for wikipedia operations."""
    MAX_WIKI_PINGS = 3

    @classmethod
    def get_wikipedia_page_text(cls, location_name: str):
        """Method to get the content from the wikipedia page."""
        search_txt = location_name
        max
        while True:
            try:
                if "," in search_txt:
                    search_txt = location_name.split(",")[0].strip()
                wiki_page = wikipedia.page(search_txt, auto_suggest=False)
                return wiki_page.content
            except (exceptions.PageError, exceptions.DisambiguationError):
                if cls.MAX_WIKI_PINGS == 0:
                    break# Try max 3 searches on wiki, else exit method.
                # Multiple pages or No page
                if "," in location_name:
                    search_txt = location_name.split(",")[1].strip()  # use country name
                else:
                    # use both city and country without a comma
                    search_txt = location_name.replace(",", "")
                cls.MAX_WIKI_PINGS -= 1
            except exceptions.WikipediaException as e:
                # Need this exception to be handled for the game to continue.
                break
