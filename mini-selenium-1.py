
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import csv

options = Options()
service = Service("geckodriver.exe")
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://www.adamchoi.co.uk/overs/detailed")

result_button = driver.find_element(
    By.XPATH, '//label[@analytics-event="All matches"]')
result_button.click()

matches = driver.find_elements(By.TAG_NAME, 'tr')

date = []
home_team = []
score = []
away_team = []


for match in matches:
    date.append(match.find_element(By.XPATH, './/td[1]').text)
    home_team.append(match.find_element(By.XPATH, './/td[3]').text)
    score.append(match.find_element(By.XPATH, './/td[4]').text)
    away_team.append(match.find_element(By.XPATH, './/td[5]').text)

with open("matches.csv", "w", newline='', encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Home Team', 'Score', 'Away Team'])
    writer.writerows(rows)

driver.quit()
print("File Saved")
