from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from random import choice

address = os.path.abspath(__file__)
address = os.path.dirname(address)
address = os.path.join(address, 'geckodriver.exe')

options = Options()
service = Service(executable_path=address)
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://www.saucedemo.com/")


username = ["standard_user",
            "locked_out_user",
            "problem_user",
            "performance_glitch_user",
            "error_user",
            "visual_user"]
try:

    Username = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "user-name")))
    Username.send_keys(choice(username))

    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce"+Keys.ENTER)

    WebDriverWait(driver, 5).until(EC.any_of(
        EC.url_contains("https://www.saucedemo.com/inventory.html"),
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    ))

    if "inventory.html" in driver.current_url:
        print("Login is successful")

    else:
        erro_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
        print(f"Login is faild : {erro_msg}")

except Exception as e:
    print(f"ERROR {e}")
