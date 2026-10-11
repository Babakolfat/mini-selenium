import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

address = os.path.dirname(os.path.abspath(__file__))
address = os.path.join(address, "geckodriver.exe")

service = Service(executable_path=address)
driver = webdriver.Firefox(service=service)

try:
    driver.get("https://www.saucedemo.com/")

    # ----------- LOGIN -----------
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.ID, "user-name"))).send_keys("standard_user")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.ID, "password"))).send_keys("secret_sauce" + Keys.ENTER)

    # ----------- Check -----------
    WebDriverWait(driver, 5).until(EC.any_of(
        EC.url_contains("inventory.html"),
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    ))

    if "inventory.html" in driver.current_url:
        print("Login Successful")
    else:
        erro_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
        print(f"Login is Failed: {erro_msg}")

    # ----------- Inventory -----------
    items_name = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name")))
    items_desc = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_desc")))
    items_price = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_price")))

    for name, desc, price in zip(items_name, items_desc, items_price):
        print(f"{name.text} : {desc.text}\n --{price.text}--\n")

    # ----------- Add to cart -----------
    count_ = 0
    loop = True
    while loop:
        items = input("Please type your items and add your items in Shopping Cart (done - shopping cart): ")

        if items.lower() == "done":
            print("exit")
            loop = False
            continue

        item_list = [item.strip().lower() for item in items.split(",")]
        for item in item_list:
            buttons = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.btn_inventory")))

            found = False
            for button in buttons:
                button_name = button.get_attribute("name").replace("-", " ")
                if item in button_name:
                    button.click()
                    print("Your Item successfully added")
                    count_ += 1
                    found = True
                    break
            if not found:
                print("Can't find")

    # ------------------------------
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "shopping_cart_link"))).click()

    # -------- check ----------
    WebDriverWait(driver, 5).until(EC.url_contains("cart.html"))

    if "cart.html" in driver.current_url:
        print("we in cart")
    else:
        print("can't go please check your internet")

    cart_items = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name")))
    cart_items = [item.text for item in cart_items]

    def checkout(firstname, lastname, zip_code):
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "checkout"))).click()

        WebDriverWait(driver, 5).until(EC.url_contains("checkout-step-one.html"))

        if "checkout-step-one.html" in driver.current_url:
            print("we in Checkout")
        else:
            print("can't go please check your internet")

        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.ID, "first-name"))).send_keys(firstname)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.ID, "last-name"))).send_keys(lastname)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.ID, "postal-code"))).send_keys(zip_code)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "continue"))).click()

    def last_step():
        labels = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[contains(@class,"summary_info_label") or '
                       'contains(@class,"summary_value_label") or '
                       'contains(@class,"summary_subtotal_label") or '
                       'contains(@class,"summary_tax_label") or '
                       'contains(@class,"summary_total_label")]')))
        for i in labels:
            print(i.text)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "finish"))).click()
        print("Your order has been dispatched, and will arrive just as fast as the pony can get there!")

    loop_2 = True
    while loop_2:
        NotWant = input("Are you want to remove item? ").lower()
        if NotWant == "yes":
            print(f"{cart_items}\n")
            which_want = int(input("which item you remove (by number)? "))
            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(
                (By.XPATH, f'//div[@class="cart_item"]//button'))
            )[which_want - 1].click()
        else:
            checkout("akbar", "agomad", "134")
            last_step()
            loop_2 = False

except Exception as e:
    print(f"Your Error is - {e}")

finally:
    driver.quit()