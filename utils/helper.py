from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import random

def wait_for_page_load(driver, timeout=120):
    """Wait until the page has fully loaded. Reload the browser if the initial timeout is exceeded, then continue waiting."""
    logging.info("Waiting for the page to load.")
    
    start_time = time.time()
    reload_done = False
    
    while True:
        # Check if the page is loaded
        if driver.execute_script("return document.readyState") == "complete":
            logging.info("Page has fully loaded.")
            return
        # Check if timeout has been exceeded
        if time.time() - start_time > timeout:
            if not reload_done:
                logging.warning("Timed out waiting for the page to load. Reloading browser.")
                reload_browser(driver)
                start_time = time.time()  # Reset start time after reload
                reload_done = True
            else:
                logging.error("Page failed to load after reload.")
                break
        
        logging.debug("Page not fully loaded yet. Checking again in 1 second.")
        random_sleep()

def reload_browser(driver):
    """Reload the current page in the browser."""
    try:
        driver.refresh()  # Refresh the current page
        logging.info("Browser refreshed successfully.")
    except Exception as e:
        logging.error(f"Error refreshing browser: {e}")

def random_sleep():
    """
    Sleep for a random duration between 1 and 5 seconds.
    """
    duration = random.uniform(3, 5)  # seconds
    time.sleep(duration)