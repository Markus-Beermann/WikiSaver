"""Module to load the environment parameters."""
import os
from dotenv import load_dotenv


class LoadEnvironment:
    """Class to load the environment parameters."""
    __OPENAI_API_KEY = ""
    __GENAI_API_KEY = ""

    def __init__(self):
        load_dotenv()
        self.__OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.__GENAI_API_KEY = os.getenv("GENAI_API_KEY")

    @property
    def open_api_key(self):
        """Animal API Key"""
        return self.__OPENAI_API_KEY

    @property
    def genai_api_key(self):
        """Animal API Key"""
        return self.__GENAI_API_KEY
