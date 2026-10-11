from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

service = Service(executable_path="geckodriver.exe")
driver = webdriver.Firefox(service=service)

driver.get("https://www.google.com/")

google = driver.find_element(
    By.XPATH, "/html/body/div[2]/div[4]/form/div[1]/div/div[1]/div[1]/div[3]/div/div[2]")

google.click()

time.sleep(1)

driver.execute_script("window.open();")

time.sleep(1)

driver.switch_to.window(driver.window_handles[1])

time.sleep(1)

driver.get("https://workspace.google.com/intl/fa/products/calendar/")
varzesh = driver.find_element(
    By.XPATH, '//*[@id="root"]/gws-dynamic-module-container/div[2]/gws-header/header/div[2]/div[1]/details[1]/summary')

varzesh.click()
