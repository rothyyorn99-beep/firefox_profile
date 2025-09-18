from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from utils.helper import wait_for_page_load, reload_browser
def is_admin(driver, admin_name, timeout=10):
    """
    Click the admin profile on Facebook. Returns True if clicked successfully, False otherwise.
    Handles spaces, normalize-space, and multiple possible matches.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    print(f"[is_admin] Going to click admin: {admin_name}")

    try:
        # Click "Your profile" first
        profile_btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Your profile' or @aria-label='Profile']"))
        )
        profile_btn.click()
        time.sleep(2)

        # Try clicking admin name using normalize-space
        button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//*[@aria-label='Switch to {admin_name}']"))
        )

        # Click using JavaScript for reliability
        driver.execute_script("arguments[0].click();", button)

        time.sleep(5)  # Wait for the profile switch to take effect
        
        return True
        

    except Exception as e:
        print(f"[is_admin] Could not click admin '{admin_name}': {e}")
        return False

def access_page(driver, page_id):
    try:
        wait_for_page_load(driver)
        driver.get(f'https://web.facebook.com/profile.php?id={page_id}')
        logging.info("Home page refreshed.")
        wait_for_page_load(driver)
        switch_page(driver)
    except Exception as e:
        logging.error(f"Error refreshing home page: {e}")
        
def switch_page(driver):
    try:
        try:
            Switch_element_now = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//div[@aria-label='Switch Now'])"))
            )
            Switch_element_now.click()
        except Exception:
            logging.info("Trying alternative switch method.")
            Switch_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//div[@aria-label='Switch'])"))
            )
            Switch_element.click()
        
            Switch_element2 = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "(//div[@aria-label='Switch'])[2]"))
            )
            Switch_element2.click()
    except Exception as e:
        logging.error(f"Error switching profile on page : {e}")