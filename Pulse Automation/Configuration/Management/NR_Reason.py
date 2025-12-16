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

    # ================= NR REASON =================
    print("📌 Opening NR Reason tab...")
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[normalize-space()='NR Reason']")
        ))
    )

    time.sleep(2)

    print("➕ Clicking Add NR Reason button...")
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(.,'Add NR Reason')]")
        ))
    )

    print("✍️ Entering Reason Code...")
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='reasonCode']")
    )).send_keys("001")

    print("✍️ Entering Reason Name...")
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='reasonName']")
    )).send_keys("Not Reachable - Automation")
    time.sleep(10)
    # ================= CLICK LAST "Add" BUTTON =================
    print("✅ Clicking the final 'Add' button...")
    wait = WebDriverWait(driver, 10)
    add_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//button[@type='submit' and .//span[text()='Add']])[last()]")
    ))
    add_button.click()

except TimeoutException as e:
    print("❌ Timeout Error:", e)

finally:
    time.sleep(5)
    # driver.quit()
