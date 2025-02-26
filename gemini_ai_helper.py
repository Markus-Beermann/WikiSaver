import google.generativeai as genai
from load_enviorments import LoadEnvironment
from print_helpers import PrintHelper

class GeminiAIHelper:
    def __init__(self):
        self.__le = LoadEnvironment()
        self.__key = self.__le.genai_api_key

        if self.__key:
            self.__active = True
            genai.configure(api_key=self.__key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            # models = genai.list_models()
            # for model in models:
            #     print(model.name, " - ", model.supported_generation_methods)

            #'models/gemini-1.0-pro-vision-latest'
            #'models/gemini-pro-vision'
            #'models/gemini-1.5-pro-latest'
            self.__genai_model = model
        else:
            self.__active = False
            self.__genai_model = None

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
            if "," in target_capital:
                target_capital = target_capital.split(",")[0].strip()

            prompt = (
                f"Find all Wikipedia pages that list world capitals and check which of them mention {target_capital}. "
                f"Return a list of Wikipedia page URLs where {target_capital} is explicitly mentioned in the context of capitals or related geopolitical topics."
            )
            response = self.__genai_model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            PrintHelper.pr_error(f"Unable to retrieve Wikipedia references. {str(e)}")

    def get_travel_options(self, location, target):
        """Generates travel advice from OpenAI about the best way to travel between two locations."""
        try:
            if not self.active:
                return None
            prompt = f"I am in {location}. My goal is to reach {target}. What is the best way to travel next?"
            response = response = self.__genai_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            PrintHelper.pr_error(f"Unable to retrieve travel advice. {str(e)}")

