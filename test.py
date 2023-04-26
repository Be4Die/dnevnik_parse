from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pathlib import Path
import time

url = "https://login.dnevnik.ru/login/esia/astrakhan"
url_1 = "https://www.youtube.com/watch?v=LnMq8s_vADo"
chrome_driver_path = Path("./chrome_driver/chromedriver.exe")
service = Service(str(chrome_driver_path.absolute()))
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(url=url)
    time.sleep(5)
    driver.get(url=url_1)
    time.sleep(1000)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
