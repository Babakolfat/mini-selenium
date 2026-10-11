from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
import os
import time
import re
import csv

address = os.path.abspath(__file__)
address = os.path.dirname(address)
address = os.path.join(address, "geckodriver.exe")


service = Service(executable_path=address)
driver = webdriver.Firefox(service=service)

driver.get("https://www.digikala.com/")

PATTERN = re.compile(r"(?:[A-Za-z0-9._%+-]+@(yahoo|gmail|outlook)\.com)"
                     r"|"
                     r"(?:(?:\+98|0098|98|0)?9[0-9]{9})", re.IGNORECASE)


def signup_login():
    """ Username must be a phone number or email, otherwise you will not be able to log in properly.  """

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.XPATH, '//button[contains(., "ورود")] | //a[contains(., "ورود")]'))).click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username")))

    while True:

        username = input("Please enter your phone number or email: ")

        if PATTERN.fullmatch(username):
            break

        time.sleep(4)
        print("Your Phone number or email is not true")

    time.sleep(6)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.ID, "username"))).send_keys(username + Keys.ENTER)

    try:

        code_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "code")))

    except TimeoutException:
        print("Code field did not appear")

    code = input("Enter the verification code: ").strip()
    code_field.send_keys(code + Keys.ENTER)

    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.ID, "code")))  # FIX 2: name
        print("Login successful")
    except TimeoutException:
        print("Login Failed (wrong code?)")


def search():
    research = input("What product would you like to search? ").strip()

    driver.get("https://www.digikala.com/search/?q=" + quote(research))

    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="ProductListPagesWrapper"]')))

    loop = True
    while loop:
        sort = input(
            "The default sorting for this site is 'most relevant.' Would you like to choose a different sorting ? ").lower()

        def ifyes():
            sort2 = int(input("Sort by (left to right): Most Viewed, Newest, Best-Selling, Lowest Price, Highest Price, Fastest, Buyers' Recommendations, and Featured. Enter a number to apply the sorting order. -- "))
            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="ProductListPagesWrapper"]/section[1]/div[1]/div/div/div/div[2]//span')))[sort2 - 1].click()
            time.sleep(3)  # wait for the products

        def scrapitems():

            CARD = '//div[@data-testid="product-card"]'

            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, CARD)))

            items = int(
                input("How many products would you like us to display(max 20)? "))

            seen = []
            rows = []
            count = 0
            tries = 0

            while count < items and tries < 30:
                for card in driver.find_elements(By.XPATH, CARD):
                    link = card.find_element(
                        By.XPATH, "./ancestor::a").get_attribute("href")
                    if link in seen:
                        continue
                    seen.append(link)

                    name = card.find_element(
                        By.XPATH, ".//h3").get_attribute("textContent").strip()
                    rating = card.find_element(
                        By.XPATH, ".//p[contains(@class,'text-body2-strong')]").get_attribute("textContent").strip()
                    price = card.find_element(
                        By.XPATH, ".//span[@data-testid='price-final']").get_attribute("textContent").strip()

                    count += 1
                    print(count, name, rating, price)
                    rows.append([count, name, rating, price])
                    if count == items:
                        break

                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(1)
                tries += 1

            save = input(
                "Do you want to save results in a CSV file? (yes/no) ").strip()
            if save == "yes":

                path = os.path.abspath(__file__)
                path = os.path.dirname(path)
                path = os.path.join(path, "digikala.csv")

                with open(path, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Number", "Name", "Rating", "Price"])
                    writer.writerows(rows)
                    print("File Saved")

        if sort == "yes":
            ifyes()
            scrapitems()
        else:
            scrapitems()

        break


user = input("You want to login or no? ").lower()
if user == "yes":
    signup_login()
    search()
else:
    search()
