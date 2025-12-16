from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# ---- Setup ----
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://pulsevideo.pulsecx.app/login")

wait = WebDriverWait(driver, 30)

try:
    # ================= LOGIN =================
    print("🔐 Logging in...")

    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='userName']")
    )).send_keys("syed.muneeb")

    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='password']")
    )).send_keys("Agent@123")

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[@for='loginAsSupervisor']")
        ))
    )

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Login']")
        ))
    )

    print("✅ Login successful")
    time.sleep(5)

    # ================= NAVIGATION =================
    print("📂 Navigating to Calendar...")

    management_title = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[normalize-space()='MANAGEMENT']")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", management_title)
    time.sleep(1)

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space()='Configuration']")
        ))
    )

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@href,'/configuration/management')]")
        ))
    )

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@href,'/calendar')]")
        ))
    )

    # ================= ADD NEW CALENDAR =================
    print("➕ Adding new calendar...")

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//text()[contains(.,'Add New')]]")
        ))
    )

    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='calendarName']")
    )).send_keys("Automation Calendar")

    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='description']")
    )).send_keys("Calendar created via Selenium automation")

    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='startDate']")
    )).send_keys("16-12-2025")

    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='endDate']")
    )).send_keys("11-11-2026")

    # ================= FIXED TIME INPUTS =================
    start_time = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@formcontrolname='startTime']")
        )
    )
    driver.execute_script("""
        arguments[0].focus();
        arguments[0].value = '21:00';
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].blur();
    """, start_time)

    end_time = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@formcontrolname='endtime']")
        )
    )
    driver.execute_script("""
        arguments[0].focus();
        arguments[0].value = '18:00';
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].blur();
    """, end_time)

    # ================= SUBMIT =================
    add_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit' and normalize-space()='Add']")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", add_btn)

    print("✅ Calendar added successfully")

except TimeoutException as e:
    print("❌ Timeout Error:", e)

finally:
    time.sleep(5)
    # driver.quit()
