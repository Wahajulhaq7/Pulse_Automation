import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

# Directory for screenshots
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_add_nr_reason(driver, request):
    wait = WebDriverWait(driver, 30)
    driver.get("https://pulsevideo.pulsecx.app/login")
    
    try:
        # ========== LOGIN ==========
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='userName']"))).send_keys("syed.muneeb")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='password']"))).send_keys("Agent@123")

        driver.execute_script(
            "arguments[0].click();",
            wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='loginAsSupervisor']")))
        )
        driver.execute_script(
            "arguments[0].click();",
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Login']")))
        )
        time.sleep(5)

        # ========== NAVIGATION ==========
        driver.execute_script("arguments[0].scrollIntoView(true);", wait.until(EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='MANAGEMENT']"))))
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Configuration']"))))
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/configuration/management')]"))))
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/calendar')]"))))

        # ========== NR REASON ==========
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='NR Reason']"))))
        time.sleep(2)
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Add NR Reason')]"))))

        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='reasonCode']"))).send_keys("NR001")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='reasonName']"))).send_keys("Not Reachable - Automation")

        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and .//span[text()='Add']]")))
        add_button.click()

        time.sleep(2)
        # Assert success: you can replace this with actual success message check
        success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Successfully added')]")))
        assert success_message.is_displayed(), "NR Reason not added successfully"

    except Exception as e:
        # Take screenshot on failure
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"failure_{int(time.time())}.png")
        driver.save_screenshot(screenshot_path)
        # Attach screenshot to pytest-html report
        if hasattr(request.node, "add_report_section"):
            request.node.add_report_section("call", "screenshot", f'<img src="{screenshot_path}" width="600">')
        raise e
