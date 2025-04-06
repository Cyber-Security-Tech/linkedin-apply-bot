import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

load_dotenv()

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

print("🔗 Opening LinkedIn...")
driver.get("https://www.linkedin.com/login")

# Login
email_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")
email_input.send_keys(EMAIL)
password_input.send_keys(PASSWORD)
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
print("✅ Logged in successfully!")

# Navigate to jobs
driver.get("https://www.linkedin.com/jobs/search/?keywords=python%20developer")
time.sleep(3)

print("🔎 Scrolling to load jobs...")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

print("📦 Waiting for job cards...")
job_cards = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job-card-container"))
)

print(f"\n📄 Found {len(job_cards)} jobs:\n")
for i, card in enumerate(job_cards[:10], 1):
    try:
        title = card.find_element(By.CSS_SELECTOR, "a.job-card-container__link").text.strip()
    except:
        title = "N/A"

    try:
        company = card.find_element(By.CSS_SELECTOR, ".artdeco-entity-lockup__subtitle span").text.strip()
    except:
        company = "N/A"

    try:
        location = card.find_element(By.CSS_SELECTOR, ".job-card-container__metadata-wrapper li span").text.strip()
    except:
        location = "N/A"

    try:
        link = card.find_element(By.CSS_SELECTOR, "a.job-card-container__link").get_attribute("href")
    except:
        link = "N/A"

    print(f"{i}. {title}\n   {company} | {location}\n   🔗 {link}\n")

input("⏸️ Press ENTER to quit browser...")
driver.quit()
