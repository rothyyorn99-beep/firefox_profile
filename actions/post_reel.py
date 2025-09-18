from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os
import random
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from utils import *


def post_reel(driver, folder_path, desc, is_use_file_name, is_random, total_videos):

    folder_path = folder_path  # Use raw string for Windows paths
        
    try:
        # # random_files = get_random_file_paths(folder_path, 3)
        # random_files = get_file_paths(folder_path, total_videos)
        if is_random is True:
            videos_to_upload = get_random_file_paths(folder_path, total_videos)
        else:
            videos_to_upload = get_file_paths(folder_path, total_videos)

        
        
        
        print(f"file: {videos_to_upload}")
        
        # time.sleep(10000)
        # reel_count_pass = 0  # Initialize the click counter
        # reel_count_fail = 0
        
        for file_path in videos_to_upload:
            print(file_path)
            #Decide description
            if is_use_file_name is True:
                description = get_file_name_without_extension(file_path)
            else:
                description = desc
            print(f"desc: {description}")
            try:
               
                # reel(driver, file_path)
                # time.sleep(100000)
                try:
                    try:
                        driver.get('https://web.facebook.com/reels/create/?surface=ADDL_PROFILE_PLUS')
                        logging.info("Home page refreshed.")
                    except Exception as e:
                        logging.error(f"Error refreshing home page: {e}")
                    wait_for_page_load(driver)
                
                    create_reel_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Create a reel")]'))
                    )
                    create_reel_btn.click()
                    wait_for_page_load(driver)
                     # try:
                
                    file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                    file_input.send_keys(file_path)
                                # wait_for_page_load(driver)
                    # except Exception as e:
                    #     logging.error(f"Error refreshing home page: {e}")
                    wait_for_page_load(driver)
                    # try:
                            # Wait for the 'Next' button to become clickable
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
                    )
                                # Click the 'Next' button
                    next_button.click()
                    # except Exception as e:
                    #     logging.error(f"Error clicking 'Next' button: {e}")
                    
                    wait_for_page_load(driver)
                    # try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "(//div[@aria-label='Next'])[2]"))
                    )
                                # Click the "Next" button
                    next_button.click()
                    print("Successfully clicked the 'Next' button in the modal dialog.")
                    # except Exception as e:
                    #     print(f"An error occurred: {e}")
                    time.sleep(1)

                    wait_for_page_load(driver)
                    try:
                        add_text = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[@aria-placeholder='Describe your reel...']"))
                        )
                        add_text.click()  # focus the div

                        # Loop through each character to mimic typing
                        for char in description:
                            add_text.send_keys(char)
                            time.sleep(random.uniform(0.05, 0.2))  # random delay between keystrokes

                        time.sleep(0.3)
                        add_text.send_keys(Keys.RETURN)  # optional: press Enter
                        
                        print("Description typed like a real user!")
                    except Exception as e:
                        print("Failed to type description:", e)

                
                
                    # Wait until the second 'Next' button is located
                    Click_public = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Publish' and not(@aria-disabled='true')]"))
                    )
                    
                    # Click the button after it becomes enabled
                    Click_public.click()  
                    wait_for_page_load(driver)
                    # Set the timeout duration in seconds
                    timeout_duration = 40  # 3 minutes
                    check_interval = 1  # Check every 5 seconds
                    start_time = time.time()  # Record the start time
                    desired_text = "Create reel"
                    try:
                        # Loop until the desired text is found or the timeout is reached
                        while True:
                            try:
                                try:
                                    time.sleep(1)
                                    WebDriverWait(driver, check_interval).until(
                                        EC.presence_of_element_located((By.XPATH, "//a[@href='/reels/create/']//span[contains(text(), 'Create reel')]"))
                                    )
                                    # Locate the results description element
                                    results_description = driver.find_element(By.XPATH, "//a[@href='/reels/create/']//span[contains(text(), 'Create reel')]")
                                    
                                
                                    
                                except Exception as e:
                                    # driver.set_window_size(800, 800)
                                    WebDriverWait(driver, check_interval).until(
                                        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Share']"))
                                    )
                                        # Locate the results description element
                                    results_description = driver.find_element(By.XPATH, "//div[@aria-label='Share']")
                                # results_description = WebDriverWait(driver, check_interval).until(
                                # EC.presence_of_element_located((By.XPATH, '//div[@aria-label='Share']'))
                                # )
                                print(f"Status: Found {results_description.text}")
                                # Check the text inside the results description
                                if results_description.text == "Like" or results_description.text == "Create reel":
                                    print(f"Status: Found {results_description.text}")
                                        
                                
                                    break  # Exit the loop if the desired text is found
                                else:
                                    print(f"Current Status:", {results_description.text})
                            except NoSuchElementException:
                                print("Results description element not found, retrying...")
                            # Check for timeout
                            elapsed_time = time.time() - start_time
                            if elapsed_time >= timeout_duration:
                                print("Timeout reached: 3 minutes have passed without finding 'No issues found'.")
                                break
                            time.sleep(check_interval)  # Wait for the specified check interval
                    except Exception as e:
                        print(f"posted not pulling waiting")
                        time.sleep(1)      
                except Exception as e:

                    home_btn = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Facebook']"))
                        )
                    home_btn.click()
                    time.sleep(7)
                    create_reel_btn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[text()='Reel']/ancestor::div[@role='button']"))
                    )
                    create_reel_btn.click()
                    logging.info("Home page refreshed.")
                    time.sleep(7)
                    file_input = driver.find_element(By.XPATH, "(//input[@type='file' and contains(@accept,'video')])[2]")
                    file_input.send_keys(file_path)
                    
                    try:
                        next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
                        )
                                
                        next_button.click()
                        print("Clicked next after upload")
                    except Exception as e:
                        print(f"An error occurred: No next button")
                    try:
                        add_text = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[@aria-placeholder='Describe your reel...']"))
                        )
                        add_text.click()  # focus the div

                        # Loop through each character to mimic typing
                        for char in description:
                            add_text.send_keys(char)
                            time.sleep(random.uniform(0.05, 0.2))  # random delay between keystrokes

                        time.sleep(0.3)
                        add_text.send_keys(Keys.RETURN)  # optional: press Enter
                        
                        print("Description typed like a real user!")
                    except Exception as e:
                        print("Failed to type description:", e)
                    # time.sleep(1000)
                    # wait_for_page_load(driver)
                    try:
                        next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "(//span[text()='Next'])[2]"))
                        )
                                
                        next_button.click()
                        print("clicked next(//span[text()='Next'])[2] after desc")
                    except Exception as e: 
                        print(f"An error occurred: No fount (//span[text()='Next'])[2]  button")
                    time.sleep(15)
                    try:
                        post_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[text()='Post']"))
                        )
                                
                        post_btn.click()
                        print("clicked //span[text()='Post']")
                    except Exception as e: 
                        print(f"An error occurred: No fount post button")
                    
                    


                time.sleep(5)
                # reel_count_pass += 1  # Increment the counter after a successful click
            except Exception as e:
                # reel_count_fail += 1  # Increment the counter after a successful click
                print(f"An error occurred: {e}")        
                
                
        # return f"Success : {reel_count_pass}, Fail : {reel_count_fail}"  # Return formatted string
    except Exception as e:
        
        print(f"An error occurred: {e}")
        driver.get('https://web.facebook.com')
            # log_action(profile, action_name, f"Error {click_count}", logger)
            # return action_name 

def get_file_name_without_extension(file_path):

    # Check if the provided path is a valid file
    if not os.path.isfile(file_path):
        raise ValueError(f"The path '{file_path}' does not point to a valid file.")
    
    # Get the file name and split it into name and extension
    file_name, _ = os.path.splitext(os.path.basename(file_path))
    return file_name   

def get_random_file_paths(folder_path, num_files=3):
    # List all files in the folder
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Check if there are enough files in the folder
    if len(all_files) < num_files:
        raise ValueError("Not enough files in the folder")

    # Randomly select num_files files
    selected_files = random.sample(all_files, num_files)
    
    return selected_files        

def get_file_paths(folder_path, num_files=3):
    # List all files in the folder
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Check if there are enough files in the folder
    if len(all_files) < num_files:
        raise ValueError("Not enough files in the folder")

    # Select the first `num_files` files instead of random ones
    selected_files = all_files[:num_files]
    
    return selected_files

def reel(driver, file_path):
    
    home_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Facebook']"))
        )
    home_btn.click()
    wait_for_page_load(driver)
    try:
        create_reel_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Reel']/ancestor::div[@role='button']"))
        )
        create_reel_btn.click()
        logging.info("Home page refreshed.")
        time.sleep(7)

        file_input = driver.find_element(By.XPATH, "(//input[@type='file' and contains(@accept,'video')])[2]")
        file_input.send_keys(file_path)
        wait_for_page_load(driver)
        next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
                )
                            # Click the 'Next' button
        next_button.click()
    
    except Exception as e:
        logging.error(f"Error refreshing home page: {e}")
    wait_for_page_load(driver)
    time.sleep(1)
    