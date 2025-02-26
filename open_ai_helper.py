import openai
from load_enviorments import LoadEnvironment
from print_helpers import PrintHelper

class OpenAIHelper:
    def __init__(self):
       self.__le = LoadEnvironment()
       self.__key = self.__le.open_api_key
       if not self.__key:
           self.__active = False

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, val):
        self.__active = val

    def get_wikipedia_links(self, target_capital):
        """Method to find Wikipedia pages that list world capitals and checks if they mention the target capital."""
        try:
            if not self.active:
                return None

            client = openai.OpenAI(api_key=self.__key)  # Create an OpenAI client
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "You are an AI assistant that finds Wikipedia references about world capitals."},
                    {"role": "user",
                     "content": f"Find all Wikipedia pages with the mention of {target_capital}. Return a list of Wikipedia page URLs where {target_capital} is explicitly mentioned."}
                ]
            )

            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            PrintHelper.pr_error(f"Error: Unable to retrieve Wikipedia references. {str(e)}")


    def get_travel_options(self, location, target):
        """Generates travel advice from OpenAI about the best way to travel between two locations."""
        try:
            if not self.active:
                return None

            client = openai.OpenAI(api_key=self.__key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a travel guide helping users navigate between global locations."},
                    {"role": "user", "content": f"I am in {location}. My goal is to reach {target}. What is the best way to travel next?"}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            PrintHelper.pr_error(f"Error: Unable to retrieve travel advice. {str(e)}")

