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

def select_mat_dropdown(dropdown_xpath, option_text):
    """
    Opens a mat-select dropdown and selects an option by visible text.
    Assumes dropdown is already rendered and clickable.
    """
    # Click the mat-select to open
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
    driver.execute_script("arguments[0].click();", dropdown)

    # Wait for overlay with options to appear
    option_xpath = f"//span[@class='mat-option-text' and normalize-space()='{option_text}']"
    option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
    driver.execute_script("arguments[0].click();", option)

try:
    # ================= LOGIN =================
    print("🔐 Logging in...")

    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='userName']")
    )).send_keys("syed.muneeb")

    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='password']")
    )).send_keys("Agent@123")

    # Click supervisor login checkbox
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='loginAsSupervisor']")))
    )

    # Click Login button
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Login']")))
    )

    print("✅ Login successful")

    # ================= NAVIGATION =================
    print("📂 Navigating to Dial Rule Management...")

    # Wait for sidebar to load
    wait.until(EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='MANAGEMENT']")))

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Configuration']")))
    )

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/configuration/management')]")))
    )

    # Click Dial Rule tab
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@routerlink,'dial-rule-management')]")))
    )

    # Click Add Dial Rule
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-ar-dial-rule')]")))
    )

    print("✍️ Entering Dial Rule details...")

    # Fill basic fields
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='dialName']"))).send_keys("Auto Dial Rule 1")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='totalTries']"))).send_keys("3")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='day1']"))).send_keys("1")

    # ✅ STEP 1: Click the checkbox to ADD a retry rule
    print("☑️ Clicking 'Add Retry' checkbox...")
    checkbox_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='retriesFormArray0']")))
    driver.execute_script("arguments[0].click();", checkbox_label)

    # ✅ STEP 2: WAIT for the dynamic form fields to appear (CRITICAL!)
    print("⏳ Waiting for dynamic retry fields to render...")
    wait.until(EC.presence_of_element_located((By.XPATH, "//mat-select[@formcontrolname='interval' and @id='interval0']")))
    wait.until(EC.presence_of_element_located((By.XPATH, "//mat-select[@formcontrolname='graceTime' and @id='graceTime0']")))
    wait.until(EC.presence_of_element_located((By.XPATH, "//mat-select[@formcontrolname='finalState' and @id='finalState0']")))

    # ✅ STEP 3: Now safely interact with dropdowns
    print("🔽 Selecting Interval...")
    select_mat_dropdown("//mat-select[@id='interval0']", "15 mins")

    print("🔽 Selecting Grace Time...")
    select_mat_dropdown("//mat-select[@id='graceTime0']", "15 mins")

    print("🔽 Selecting Final State...")
    select_mat_dropdown("//mat-select[@id='finalState0']", "No Contact")

    print("✅ Dial Rule form filled successfully.")

except TimeoutException as e:
    print("❌ Timeout Error:", str(e))
    # Optional: take screenshot for debugging
    driver.save_screenshot("error_timeout.png")

except Exception as e:
    print("💥 Unexpected error:", str(e))
    driver.save_screenshot("error_general.png")

finally:
    print("🔚 Keeping browser open for 10 seconds...")
    time.sleep(10)
    driver.quit()