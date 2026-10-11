from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

address = os.path.abspath(__file__)
address = os.path.dirname(address)
address = os.path.join(address, 'geckodriver.exe')

service = Service(executable_path=address)
driver = webdriver.Firefox(service=service)


driver.get("https://en.wikipedia.org/wiki/Linux")

try:

    h1 = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
    print(f"Topic : {h1}\n")

    p = WebDriverWait(driver, 5).until(
        # //p[1]
        EC.presence_of_element_located((By.XPATH, '//p[1]'))).text
    print(f"explanation: {p}")

except Exception as e:
    print(f"Error is {e}")
