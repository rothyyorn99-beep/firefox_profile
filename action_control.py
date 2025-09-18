# actions.py
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import *
from actions import *

import time

def execute_actions(driver, profile, log):
    """
    Handle 3 cases:
    - Run only Page
    - Run only Admin
    - Run Admin + Page (Page first, then Admin)
    """

    is_admin_enabled = profile.get("is_admin", False)
    is_no_page = profile.get("is_no_page", False)

    admin = profile.get("admin")
    pages = profile.get("pages", [])

    # -----------------------
    # Case 1: Only Page
    # -----------------------
    if is_no_page and not is_admin_enabled:
        if pages:
            log(f"[PAGE] Running only Page actions for profile '{profile['name']}'")
            run_page_actions(driver, profile, pages, log)
        else:
            log(f"[PAGE] No pages found for '{profile['name']}', skipping Page actions.")
        return

    # -----------------------
    # Case 2: Only Admin
    # -----------------------
    if is_admin_enabled and not pages:
        if admin:
            log(f"[ADMIN] Running only Admin actions for profile '{profile['name']}'")
            run_admin_actions(driver, profile, admin, log)
        else:
            log(f"[ADMIN] No admin config for '{profile['name']}', skipping Admin actions.")
        return

    # -----------------------
    # Case 3: Admin + Page (Page first, then Admin)
    # -----------------------
    if is_admin_enabled and is_no_page and pages:
        log(f"[PAGE] Running Page actions for profile '{profile['name']}'")
        run_page_actions(driver, profile, pages, log)

        if admin:
            log(f"[ADMIN] Running Admin actions for profile '{profile['name']}'")
            run_admin_actions(driver, profile, admin, log)
        return

    # -----------------------
    # Fallback
    # -----------------------
    log(f"[INFO] Profile '{profile['name']}' has no Admin or Page actions to run.")




# -----------------------
# Helpers
# -----------------------
def run_admin_actions(driver, profile, admin, log):
    admin_name = admin.get("name")
    admin_actions = admin.get("admin_actions", [])

    wait_for_page_load(driver)
    # if not is_admin(driver, admin_name):
    #     log(f"[ADMIN] Skipping admin actions: could not confirm '{admin_name}'")
    #     return

    for action in admin_actions:
        if not action.get("is_enable", False):
            continue

        action_type = action.get("type")
        log(f"[ADMIN] Executing '{action_type}' for profile '{profile['name']}' (Admin: {admin_name})")

        if action_type == "checkIn":
            location = action.get("location")
            desc = action.get("desc", "")
            log(f"[ADMIN] CheckIn at {location}, desc: {desc}")
            # TODO: implement actual admin_checkin
        else:
            log(f"[ADMIN] Skipping media action '{action_type}'")

        time.sleep(2)

    log(f"[ADMIN] Completed Admin actions for profile '{profile['name']}'")


def run_page_actions(driver, profile, pages, log):
    for page in pages:
        page_id = page.get("page_id")
        page_actions = page.get("page_actions", page.get("actions", []))

        if not page_actions:
            log(f"[PAGE] No actions for page {page_id}, skipping.")
            continue

        access_page(driver, page_id)
        time.sleep(5)

        for action in page_actions:
            if not action.get("is_enable", False):
                continue

            action_type = action.get("type")
            log(f"[PAGE] Executing '{action_type}' for profile '{profile['name']}' on page {page_id}")

            if action_type == "checkIn":
                location = action.get("location")
                desc = action.get("desc", "")
                log(f"[PAGE] CheckIn at {location}, desc: {desc}")
                # TODO: implement actual page_checkin
            elif action_type in ["post_reel", "post_video", "post_image"]:
                log(f"[PAGE] Posting media '{action_type}' for page {page_id}")
                post_reel(
                    driver,
                    folder_path=action.get("video_path"),
                    desc=action.get("desc", ""),
                    is_use_file_name=action.get("desc_filename", False),
                    is_random=action.get("is_random", False),
                    total_videos=action.get("total_videos", 1)
                )

            time.sleep(2)

        log(f"[PAGE] Completed Page actions for page {page_id} for profile '{profile['name']}'")




