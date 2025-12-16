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


        # ================= SKILL MANAGEMENT =================
    print("🧩 Opening Skill Management...")

    # Click Skill Management tab
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@routerlink='skill-management']")
        ))
    )
    time.sleep(2)

    print("➕ Clicking Add New button...")

    # Click Add New button
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//text()[contains(.,'Add New')]]")
        ))
    )
    time.sleep(1)

    print("✍️ Entering Skill Name...")

    # Enter Skill Name
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@formcontrolname='name']")
    )).send_keys("Auto Skill 1")

    # ================= CHANNEL DROPDOWN =================
    print("📌 Selecting Channel...")

    # Open Channel mat-select
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//mat-select")
        ))
    )

    # Select "Inbound Voice"
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='mat-option-text' and normalize-space()='Inbound Voice']")
    )).click()

    time.sleep(1)

    # ================= SKILL LEVEL SLIDER =================
    print("🎚️ Toggling Skill Level slider...")

    slider = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//mat-slider[@formcontrolname='skillLevel']")
    ))

    # Move slider to max using JS
    driver.execute_script("""
        let slider = arguments[0];
        slider.value = 1;
        slider.dispatchEvent(new Event('input'));
        slider.dispatchEvent(new Event('change'));
    """, slider)

    time.sleep(1)

    # ================= SAVE =================
    print("💾 Clicking Add button...")

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit' and .//text()[contains(.,'Add')]]")
        ))
    )

    print("✅ Skill added successfully!")
except TimeoutException as e:
    print("❌ Timeout Error:", e)

finally:
    time.sleep(5)
    # driver.quit()