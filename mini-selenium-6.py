from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import csv

address = os.path.abspath(__file__)
address = os.path.dirname(address)
address = os.path.join(address, "geckodriver.exe")

service = Service(executable_path=address)
driver = webdriver.Firefox(service=service)

try:
    driver.get("https://www.varzesh3.com/")
    links = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

    print(f"Number of links: {len(links)}")

    seen = set()
    data = []

    for link in links:
        text = link.text.strip()
        href = link.get_attribute("href")
        if text and href and href not in seen:
            seen.add(href)
            data.append([text, href])

    try:
        csv_path = os.path.join(base_dir, "links.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Text", "Url"])
            writer.writerows(data)

    except:
        print("File can't save")

except Exception as e:
    print(f"Your Error is - {e}")
