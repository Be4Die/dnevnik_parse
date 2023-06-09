from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *

from fp.fp import FreeProxy

from pathlib import Path
from dataclasses import dataclass
import time

from src.data_providers import UrlsProvider, XPathsProvider, EnvDataProvider, WebServices


@dataclass
class PeopleCardWebElement:
    """
    personal information of people with image like web elements
    """
    person_id: int
    personal_data: WebElement
    document: WebElement
    contact_data: WebElement
    worker_data: WebElement


class CoreDriver:
    """
    The class allows you to connect to websites by simulating the browser using selenium
    """

    Driver_path = Path("./chrome_driver/chromedriver.exe")

    def __init__(self, proxy: bool = False, click_delay: int = 0.5, loading_delay: int = 2.5):
        """
        Constructor of CoreDriver
        :param proxy: bool - use if you need random free proxy
        :param delay: int - delay between any actions in simulation min Value 5. A value less than this can cause errors
        """

        self.__service = Service(str(self.Driver_path.absolute()))
        self.__options = webdriver.ChromeOptions()
        self.click_delay = click_delay
        self.loading_delay = loading_delay
        if proxy:
            self.__add_proxy()
        else:
            self.Proxy = None

        self.Driver = webdriver.Chrome(service=self.__service, options=self.__options)

        print(f"[+]CoreDriver {self} init:")
        print(f"----driver_path={self.Driver_path.name}")

        print(f"----proxy={self.Proxy}")

        self.UrlsProvider = UrlsProvider()
        self.XPathsProvider = XPathsProvider()

    def __del__(self):
        """
        close selenium driver when coreDriver deleted from ram
        :return:
        """

        self.Driver.close()
        self.Driver.quit()
        print(f"[-]CoreDriver {self} del")

    def __redirectToGosuslugi(self):
        """
        redirect from dnevnik to gosuslugi login page. Need Active Dnevnik login page
        :return:
        """
        url = self.UrlsProvider.get(WebServices.Dnevnik)["login"]
        if self.Driver.current_url == url:
            login_with = self.XPathsProvider.get(WebServices.Dnevnik)["login_with_gosuslugi"]
            self.Driver.find_element(By.XPATH, login_with).click()
            time.sleep(self.loading_delay)
        else:
            raise Exception(f"[x]{self}: current driver url isn't {url}")

    def __openDnevnikLogin(self):
        """
        open Dnevnik login page
        :return:
        """

        login_url = self.UrlsProvider.get(WebServices.Dnevnik)["login"]
        self.Driver.get(login_url)
        time.sleep(self.loading_delay)

    def __loginGosuslugi(self):
        """
        login to gosuslugi account. Use Env password and login
        :return:
        """

        url = self.UrlsProvider.get(WebServices.Gosuslugi)["login"]
        if self.Driver.current_url == url:
            login_input_xpath = self.XPathsProvider.get(WebServices.Gosuslugi)["login_input"]
            login_input_element = self.Driver.find_element(By.XPATH, login_input_xpath)
            login_input_element.clear()
            login_input_element.send_keys(EnvDataProvider.get_login())
            time.sleep(self.click_delay)  # delay

            password_input_xpath = self.XPathsProvider.get(WebServices.Gosuslugi)["password_input"]
            password_input_element = self.Driver.find_element(By.XPATH, password_input_xpath)
            password_input_element.clear()
            password_input_element.send_keys(EnvDataProvider.get_password())
            time.sleep(self.click_delay)  # delay

            login_btn_xpath = self.XPathsProvider.get(WebServices.Gosuslugi)["login_btn"]
            login_btn_element = self.Driver.find_element(By.XPATH, login_btn_xpath)
            login_btn_element.click()
            time.sleep(self.loading_delay)  # delay

            try:
                later_btn_xpath = self.XPathsProvider.get(WebServices.Gosuslugi)["later_btn"]
                later_btn_element = self.Driver.find_element(By.XPATH, later_btn_xpath)
                later_btn_element.click()
                time.sleep(self.click_delay)  # delay
            except NoSuchElementException:
                pass
            finally:
                print("[i]Login to Gosuslugi success")

        else:
            raise Exception(f"[x]{self}: current driver url isn't {url}")

    def __getMaxCurrentPeoplesPages(self) -> int:
        """
        find in page 'Current Peoples' max value of 'Current Peoples' pages
        :return: pages count
        """

        url = self.UrlsProvider.get(WebServices.Dnevnik)["current_peoples"]
        self.Driver.get(url)

        time.sleep(self.loading_delay)  # delay
        max_count_xpath = self.XPathsProvider.get(WebServices.Dnevnik)["max_current_peoples"]
        counter_element = self.Driver.find_element(By.XPATH, max_count_xpath)

        return int(counter_element.text)

    def __parse_current_people_card(self, id: int) -> PeopleCardWebElement:
        """
        parse current people card and compare PeopleCardWebElement
        :return: people card like webElements
        """

        dnevnik_xpaths = self.XPathsProvider.get(WebServices.Dnevnik)
        personal_data_xpath = dnevnik_xpaths["personal_data"]
        document_xpath = dnevnik_xpaths["document"]
        contact_data_xpath = dnevnik_xpaths["contact_data"]
        worker_data_xpath = dnevnik_xpaths["worker_data"]

        people_card = PeopleCardWebElement(
            person_id=id,
            personal_data=self.Driver.find_element(By.XPATH, personal_data_xpath),
            document=self.Driver.find_element(By.XPATH, document_xpath),
            contact_data=self.Driver.find_element(By.XPATH, contact_data_xpath),
            worker_data=self.Driver.find_element(By.XPATH, worker_data_xpath)
        )

        return people_card

    def Login(self):
        """
        Login to Dnevnik use gosuslugi
        :return:
        """

        self.__openDnevnikLogin()
        self.__redirectToGosuslugi()
        time.sleep(self.loading_delay)
        self.__loginGosuslugi()

    def Parse_current_peoples(self, parse_delay: int = 6, debug: bool = False) -> [PeopleCardWebElement]:
        """
        collect all 'peoples cards' from all 'current peoples pages'
        :return: list of PeopleCardWebElements
        """

        max_peoples = self.__getMaxCurrentPeoplesPages()
        url = self.UrlsProvider.get(WebServices.Dnevnik)["current_peoples_iterations"]
        table_xpath = self.XPathsProvider.get(WebServices.Dnevnik)["current_peoples_table"]

        if debug:
            max_peoples = 1

        peoples_cards = []
        for i in range(1, max_peoples + 1):
            self.Driver.get(url + str(i))
            time.sleep(self.loading_delay)  # delay
            table_element = self.Driver.find_element(By.XPATH, table_xpath)
            print(f"[i]choose table: {table_element}")
            links = []
            for row in table_element.find_elements(By.CSS_SELECTOR, "tr"):
                try:
                    ceils = row.find_elements(By.CSS_SELECTOR, "td")
                    if len(ceils) > 0:
                        btn = ceils[-1].find_element(By.CSS_SELECTOR, "a")
                        links.append(btn.get_attribute('href'))
                except NoSuchElementException:
                    pass

            print(f"[i]former {len(links)} links start parse")
            for link in links[:1]:
                print(f"[i]open people card: {link}")
                self.Driver.get(link)
                time.sleep(self.loading_delay)  # delay
                sub = link[link.find("person="):].replace("person=", '')
                id = int(sub[:sub.find("&")])
                peoples_cards.append(self.__parse_current_people_card(id))
                time.sleep(parse_delay)

        return peoples_cards

    def __add_proxy(self):
        """
        use for add free random proxy to driver
        :return:
        """

        self.Proxy = FreeProxy(anonym=True).get()
        self.__options.add_argument(f"--proxy-server={self.Proxy}")


if __name__ == "__main__":
    driver = CoreDriver()
