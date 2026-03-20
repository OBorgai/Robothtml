# -*- coding: utf-8 -*-
# Import the WebDriver module to control the browser
from selenium import webdriver
# Import By to locate elements
from selenium.webdriver.common.by import By
# Import WebDriverWait for explicit waits
from selenium.webdriver.support.ui import WebDriverWait
# Import expected_conditions for wait conditions
from selenium.webdriver.support import expected_conditions as EC
# Import Options to configure Chrome
from selenium.webdriver.chrome.options import Options

# Configure Chrome options
chrome_options = Options()
# Optional: keep the browser open after script ends (comment out if not needed)
# chrome_options.add_experimental_option("detach", True)

# Create a Chrome WebDriver instance
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the target URL
    driver.get("https://accweb.mouv.desjardins.com/identifiantunique/securite-garantie/authentification/auth/manuel?domaineVirtuel=desjardins&langueCible=fr&navigMW=mm")

    # Create an explicit wait
    wait = WebDriverWait(driver, 20)

    # Wait for the username field to be visible
    username_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )

    # Clear and type the username
    username_input.clear()
    username_input.send_keys("testuser")

    # Wait for the password field to be visible
    password_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "password"))
    )

    # Clear and type the password
    password_input.clear()
    password_input.send_keys("Test1234")

    # Wait for the login button to be clickable
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )

    # Click the login button
    login_button.click()

    # Wait for an element that indicates the dashboard is visible
    dashboard_header = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='dashboard']"))
    )

    # Assert that the dashboard element is displayed
    assert dashboard_header.is_displayed(), "Dashboard should be visible after login"

    # Assert that the URL changed to a dashboard-like page
    assert "dashboard" in driver.current_url, "URL should contain 'dashboard' after login"

finally:
    # Close the browser
    driver.quit()
