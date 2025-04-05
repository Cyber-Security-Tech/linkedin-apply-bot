from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

# Load credentials
load_dotenv()
EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

if not EMAIL or not PASSWORD:
    raise ValueError("Please make sure LINKEDIN_EMAIL and LINKEDIN_PASSWORD are set in .env")

# Set up the driver
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 1: Go to LinkedIn Jobs page (public)
driver.get("https://www.linkedin.com/jobs/search/?keywords=python%20developer&location=United%20States&f_AL=true")
time.sleep(3)

# Step 2: Wait for overlay and remove if needed
try:
    overlay = driver.find_element(By.CLASS_NAME, "modal__overlay")
    if overlay.is_displayed():
        print("⚠️ Overlay detected. Waiting for it to disappear...")
        time.sleep(2)
        driver.execute_script("""
            document.querySelector('.modal__overlay').style.display = 'none';
        """)
        print("✅ Overlay removed via JS.")
except:
    print("✅ No overlay found.")

# Step 3: Click sign in using JS to avoid interception
try:
    sign_in_btn = driver.find_element(By.LINK_TEXT, "Sign in")
    driver.execute_script("arguments[0].scrollIntoView();", sign_in_btn)
    driver.execute_script("arguments[0].click();", sign_in_btn)
    print("✅ Clicked Sign in")
except Exception as e:
    print(f"❌ Failed to click Sign in: {e}")
    driver.quit()
    exit()

# Step 4: Fill login form
time.sleep(3)
try:
    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    print("✅ Logged in successfully!")
except Exception as e:
    print(f"❌ Login error: {e}")

# Pause to see result
input("⏸️ Press ENTER to quit browser...")
driver.quit()
