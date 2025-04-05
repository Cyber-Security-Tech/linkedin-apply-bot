import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

if not EMAIL or not PASSWORD:
    raise ValueError("Please set EMAIL and PASSWORD in your .env file.")

# Setup Chrome
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("🔗 Opening LinkedIn...")
    driver.get("https://www.linkedin.com")

    time.sleep(3)
    print("⚠️ Checking for overlay...")
    try:
        overlay = driver.find_element(By.CLASS_NAME, "modal__overlay")
        if overlay.is_displayed():
            print("⚠️ Overlay detected, attempting to dismiss with ESC key...")
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(2)
    except NoSuchElementException:
        print("✅ No overlay detected.")

    try:
        sign_in = driver.find_element(By.LINK_TEXT, "Sign in")
        sign_in.click()
        print("✅ Clicked Sign in")
    except ElementClickInterceptedException:
        print("❌ Login failed: Sign in button was blocked.")
        driver.quit()
        exit()

    time.sleep(3)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)
    print("✅ Logged in successfully!")

    print("⏳ Waiting 5 seconds before navigating to job search page...")
    time.sleep(5)

    try:
        driver.get("https://www.linkedin.com/jobs/search/?keywords=python%20developer&location=United%20States&f_AL=true")
        print("✅ Reached job search page.")
    except Exception as e:
        print(f"❌ Failed to load job search page: {e}")
        driver.quit()
        exit()

    input("⏸️ Press ENTER to quit browser...")

except Exception as e:
    print(f"❌ Unexpected error: {e}")

finally:
    driver.quit()
