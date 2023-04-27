import json
from pathlib import Path
from enum import Enum
import os


class WebServices(Enum):
    Dnevnik = "dnevnik"
    Gosuslugi = "gosuslugi"


class EnvDataProvider:
    """
    provide to env variables
    """

    @staticmethod
    def get_login():
        return os.getenv("GOSUSLUGI_LOGIN")

    @staticmethod
    def get_password():
        return os.getenv("GOSUSLUGI_PASSWORD")


class JsonDataProvider:
    """
    Base class for creation json providers
    """
    DATA_PATH = None

    def __init__(self):
        """
        open file from DATA_PATH and parse json file to rawData
        """

        if self.DATA_PATH is not None:
            if Path(self.DATA_PATH).exists():
                with open(self.DATA_PATH) as file:
                    self.rawData = json.load(file)
                    print(f"[+]{self.__class__.__name__}: init")
            else:
                raise ValueError(f"[x]{self.__class__.__name__}: file in the path {self.DATA_PATH} is not found")
        else:
            self.rawData = None


class UrlsProvider(JsonDataProvider):
    DATA_PATH = Path("./src/data/Urls.json").absolute()

    def __init__(self):
        JsonDataProvider.__init__(self)

    def get(self, service: WebServices) -> dict:
        return self.rawData[service.value]


class XPathsProvider(JsonDataProvider):
    DATA_PATH = Path("./src/data/XPaths.json").absolute()

    @staticmethod
    def FullXPathToRelative(parent: str, xpath: str) -> str:
        return xpath.replace(parent, '')

    @staticmethod
    def FullXPathsToRelatives(parent: str, xpaths: dict) -> dict:
        for key in xpaths:
            obj = xpaths[key]
            if type(obj) is str:
                xpaths[key] = XPathsProvider.FullXPathToRelative(parent, xpaths[key])
            if type(obj) is dict:
                xpaths[key] = XPathsProvider.FullXPathsToRelatives(parent, xpaths[key])

        return xpaths

    def __init__(self):
        JsonDataProvider.__init__(self)

    def get(self, service: WebServices) -> dict:
        return self.rawData[service.value]


if __name__ == "__main__":
    _service = WebServices.Dnevnik
    xPathsProvider = XPathsProvider()
    urlsProvider = UrlsProvider()
    print(xPathsProvider.get(_service))
    print(urlsProvider.get(_service))
