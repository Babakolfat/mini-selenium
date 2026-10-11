from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


profile_dir = os.path.abspath("insta")
os.makedirs(profile_dir, exist_ok=True)


options = Options()
options.add_argument("-profile")
options.add_argument(profile_dir)

service = Service(executable_path="geckodriver.exe")
driver = webdriver.Firefox(service=service, options=options)

time.sleep(5)  # صبر تا لاگین کامل بشه
driver.get("https://www.instagram.com/")

username = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.NAME, "email")))
username.send_keys("YOUR USERNAME")

password = driver.find_element(
    By.NAME, "pass")
password.send_keys("YOUR EMAIL" + Keys.ENTER)


# -------------

search = input("Enter :").split()

for i in search:
    print("name: " + i)

    if "#" == i[0]:
        driver.get(f"https://www.instagram.com/explore/tags/{i[1:]}/")
        time.sleep(3)
        print("Hashtag page opened")
    else:
        driver.get(f"https://www.instagram.com/{i}/")
        try:
            meta = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//meta[@property="og:description"]')))
            info = meta.get_attribute("content").split(" - ")[0]
            parts = info.split(",")
            followers = parts[0].strip()
            following = parts[1].strip()
            post = parts[2].strip()

            print(post)
            print(followers)
            print(following)
        except:
            continue
