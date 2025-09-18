import threading
import json
import shutil
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from action_control import execute_actions  # Import the action execution logic
# -------------------------
# Load configuration
# -------------------------
def load_config(file_name="config.json"):
    config_path = os.path.join(os.path.dirname(__file__), file_name)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

# -------------------------
# Threading & positions
# -------------------------
lock = threading.Lock()
active_threads = 0
available_positions = []

def log(message):
    """Thread-safe logging."""
    with lock:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def calculate_positions():
    """Calculate positions for multiple browser windows."""
    positions = []
    for row in range(config["screen_height"] // config["window_height"]):
        for col in range(config["per_row"]):
            pos_x = col * config["window_width"]
            pos_y = row * config["window_height"]
            if pos_x + config["window_width"] > config["screen_width"] or \
               pos_y + config["window_height"] > config["screen_height"]:
                break
            positions.append((pos_x, pos_y))
    return positions

# -------------------------
# Optional profile cleanup
# -------------------------
def clean_profile(profile_path):
    """Clean temporary Firefox folders to speed up startup."""
    if not config.get("cleanup_profiles", False):
        return
    temp_dirs = [
        "cache2", "startupCache", "jumpListCache", "thumbnails", "minidumps",
        "safebrowsing", "offlineCache", "weave", "extensions", "crashes",
        "bookmarkbackups", "sessionstore-backups", "storage", "shake",
        "siteSecurityServiceState", "spellcheck", "favicons", "gmp",
        "GPUCache", "ShaderCache", "VideoDecodeStats", "Crashpad", "DawnCache"
    ]
    for folder in temp_dirs:
        path = os.path.join(profile_path, folder)
        if os.path.exists(path):
            try:
                shutil.rmtree(path, ignore_errors=True)
            except Exception as e:
                log(f"Failed to clear {path}: {e}")


# -------------------------
# Firefox launcher
# -------------------------
def launch_firefox(profile, pos_x, pos_y):
    """Launch a Firefox profile at a specific screen position and run actions."""
    global active_threads
    profile_path = os.path.join(config["profile_base_path"], profile["name"])
    if not os.path.exists(profile_path):
        log(f"Profile {profile['name']} not found! Skipping.")
        return

    with lock:
        active_threads += 1

    try:
        start_time = time.time()
        clean_profile(profile_path)

        options = Options()
        options.profile = profile_path
        options.set_preference("browser.sessionstore.resume_from_crash", False)
        options.set_preference("browser.startup.homepage_override.mstone", "ignore")
        options.set_preference("startup.homepage_welcome_url", "about:blank")
        options.set_preference("toolkit.telemetry.enabled", False)
        options.set_preference("datareporting.healthreport.uploadEnabled", False)
        options.set_preference("datareporting.policy.dataSubmissionEnabled", False)
        options.set_preference("browser.newtabpage.activity-stream.feeds.snippets", False)
        options.set_preference("browser.newtabpage.activity-stream.telemetry", False)
        options.set_preference("extensions.getAddons.cache.enabled", False)
        options.set_preference("browser.discovery.enabled", False)
        options.set_preference("browser.aboutHomeSnippets.updateUrl", "")
        options.set_preference("extensions.enabledScopes", 0)
        options.set_preference("browser.shell.checkDefaultBrowser", False)
        options.set_preference("browser.pocket.enabled", False)
        options.set_preference("media.volume_scale", "0.0")   # Mutes all audio


        service = Service(config["geckodriver_path"])
        log(f"Launching Firefox profile: {profile['name']} at ({pos_x},{pos_y}) ...")
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_window_position(pos_x, pos_y)
        driver.set_window_size(config["window_width"], config["window_height"])
        log(f"Firefox {profile['name']} launched in {time.time() - start_time:.2f}s")

        # Open URL and wait for page load
        driver.get(config["url_to_open"])
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            log(f"{profile['name']} loaded page title: {driver.title}")
        except Exception as e:
            log(f"{profile['name']} failed to load page: {e}")
        # time.sleep(5000)
        # Execute profile actions
        execute_actions(driver, profile, log)

        # time.sleep(500)  # Keep browser open for demonstration
        driver.quit()
        log(f"Firefox {profile['name']} closed, runtime: {time.time() - start_time:.2f}s")

    finally:
        with lock:
            active_threads -= 1
            available_positions.append((pos_x, pos_y))

# -------------------------
# Main launcher
# -------------------------
def main():
    global available_positions
    available_positions = calculate_positions()
    threads = []
    next_profile = 0

    while next_profile < len(config["profiles"]) or any(t.is_alive() for t in threads):
        with lock:
            if active_threads < config["max_threads"] and next_profile < len(config["profiles"]) and available_positions:
                pos_x, pos_y = available_positions.pop(0)
                profile = config["profiles"][next_profile]
                t = threading.Thread(target=launch_firefox, args=(profile, pos_x, pos_y))
                t.start()
                threads.append(t)
                next_profile += 1
        time.sleep(10)

    for t in threads:
        t.join()

    log("All browsers are closed.")

if __name__ == "__main__":
    main()
