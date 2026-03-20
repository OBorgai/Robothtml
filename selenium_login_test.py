"""Robust Selenium login test with Chrome/Edge support."""

# -*- coding: utf-8 -*-
# Import Python logging to emit structured logs
import logging
# Import typing helpers for clearer signatures
from typing import Iterable, Tuple
# Import the WebDriver module to control the browser
from selenium import webdriver
# Import By to locate elements
from selenium.webdriver.common.by import By
# Import WebDriverWait for explicit waits
from selenium.webdriver.support.ui import WebDriverWait
# Import expected_conditions for wait conditions
from selenium.webdriver.support import expected_conditions as EC
# Import Options to configure Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
# Import Options to configure Edge
from selenium.webdriver.edge.options import Options as EdgeOptions

# Define constants for test data and timeouts
LOGIN_URL = "https://accweb.mouv.desjardins.com/identifiantunique/securite-garantie/authentification/auth/manuel?domaineVirtuel=desjardins&langueCible=fr&navigMW=mm"
# Store test username in one place
USERNAME = "testuser"
# Store test password in one place
PASSWORD = "Test1234"
# Set a default explicit wait timeout
DEFAULT_TIMEOUT = 25


# Configure the logger once for the script
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
# Create a named logger for this module
logger = logging.getLogger("selenium-login-test")


def build_driver(browser: str = "chrome") -> webdriver.Remote:
    """Create a WebDriver instance for Chrome or Edge."""
    # Normalize the browser name to avoid casing issues
    normalized_browser = browser.strip().lower()
    # Log which browser will be launched
    logger.info("Launching browser: %s", normalized_browser)
    # Prepare Chrome options when the browser is Chrome
    if normalized_browser == "chrome":
        # Initialize Chrome options
        chrome_options = ChromeOptions()
        # Optional: keep the browser open after script ends (comment out if not needed)
        # chrome_options.add_experimental_option("detach", True)
        # Create the Chrome WebDriver instance
        return webdriver.Chrome(options=chrome_options)
    # Prepare Edge options when the browser is Edge
    if normalized_browser == "edge":
        # Initialize Edge options
        edge_options = EdgeOptions()
        # Create the Edge WebDriver instance
        return webdriver.Edge(options=edge_options)
    # Raise a clear error when an unsupported browser is requested
    raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'edge'.")


def wait_for_first_visible(
    wait: WebDriverWait,
    locators: Iterable[Tuple[str, str]],
):
    """Return the first visible element among multiple locators."""
    # Iterate through the locator list in order of robustness
    for locator in locators:
        # Log which locator is being attempted
        logger.info("Trying locator: %s", locator)
        try:
            # Wait for the element to be visible
            return wait.until(EC.visibility_of_element_located(locator))
        except Exception:
            # Log locator failure and move to the next one
            logger.warning("Locator failed, trying next: %s", locator)
    # If none of the locators worked, raise a timeout error
    raise TimeoutError("None of the provided locators became visible.")


def wait_for_clickable(
    wait: WebDriverWait,
    locators: Iterable[Tuple[str, str]],
):
    """Return the first clickable element among multiple locators."""
    # Iterate through the locator list in order of robustness
    for locator in locators:
        # Log which locator is being attempted
        logger.info("Trying clickable locator: %s", locator)
        try:
            # Wait for the element to be clickable
            return wait.until(EC.element_to_be_clickable(locator))
        except Exception:
            # Log locator failure and move to the next one
            logger.warning("Clickable locator failed, trying next: %s", locator)
    # If none of the locators worked, raise a timeout error
    raise TimeoutError("None of the provided locators became clickable.")


def perform_login(driver: webdriver.Remote) -> None:
    """Run the login flow and verify the dashboard."""
    # Log the start of the navigation step
    logger.info("Navigating to login page")
    # Open the target URL
    driver.get(LOGIN_URL)
    # Create an explicit wait
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    # Define robust locators for the username field
    username_locators = [
        (By.NAME, "username"),
        (By.ID, "username"),
        (By.CSS_SELECTOR, "input[type='text'][name*='user']"),
    ]
    # Define robust locators for the password field
    password_locators = [
        (By.NAME, "password"),
        (By.ID, "password"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ]
    # Define robust locators for the login button
    login_button_locators = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(., 'Connexion') or contains(., 'Login')]"),
        (By.CSS_SELECTOR, "[data-testid='login-submit']"),
    ]
    # Wait for the username field to be visible
    username_input = wait_for_first_visible(wait, username_locators)
    # Clear and type the username
    username_input.clear()
    username_input.send_keys(USERNAME)
    # Log that the username was entered
    logger.info("Username entered")
    # Wait for the password field to be visible
    password_input = wait_for_first_visible(wait, password_locators)
    # Clear and type the password
    password_input.clear()
    password_input.send_keys(PASSWORD)
    # Log that the password was entered
    logger.info("Password entered")
    # Wait for the login button to be clickable
    login_button = wait_for_clickable(wait, login_button_locators)
    # Click the login button
    login_button.click()
    # Log that the login button was clicked
    logger.info("Login submitted")
    # Define robust locators for the dashboard area
    dashboard_locators = [
        (By.CSS_SELECTOR, "[data-testid='dashboard']"),
        (By.CSS_SELECTOR, "[data-testid*='dashboard']"),
        (By.XPATH, "//*[contains(@class, 'dashboard') or contains(., 'Tableau de bord')]"),
    ]
    # Wait for the dashboard to become visible
    dashboard_element = wait_for_first_visible(wait, dashboard_locators)
    # Wait for the URL to contain a dashboard-like keyword
    wait.until(EC.url_contains("dashboard"))
    # Assert that the dashboard element is displayed
    assert dashboard_element.is_displayed(), "Dashboard should be visible after login"
    # Assert that the URL changed to a dashboard-like page
    assert "dashboard" in driver.current_url, "URL should contain 'dashboard' after login"
    # Log the successful assertion
    logger.info("Dashboard verified successfully")


def run_login_test(browser: str = "chrome") -> None:
    """Entry point to run the login test with safe cleanup."""
    # Initialize the driver reference
    driver = None
    try:
        # Create the requested browser driver
        driver = build_driver(browser)
        # Run the login flow
        perform_login(driver)
    except Exception as exc:
        # Log any failure with full context
        logger.exception("Login test failed: %s", exc)
        # Capture a screenshot for debugging if possible
        if driver:
            try:
                # Save the screenshot with a deterministic name
                driver.save_screenshot("selenium-login-failure.png")
                # Log that the screenshot was captured
                logger.info("Screenshot saved: selenium-login-failure.png")
            except Exception:
                # Log if screenshot capture fails
                logger.warning("Failed to capture screenshot")
        # Re-raise the exception to fail the test
        raise
    finally:
        # Ensure the browser always closes
        if driver:
            # Log that the driver is shutting down
            logger.info("Closing browser")
            # Close the browser
            driver.quit()


if __name__ == "__main__":
    # Run the test in Chrome by default
    run_login_test(browser="chrome")
