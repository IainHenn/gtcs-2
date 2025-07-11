import time
import random
from selenium.webdriver.common.by import By
from selenium import webdriver
import datetime
from celery_app import app as celery_app
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_recaptcha_solver import RecaptchaSolver
import undetected_chromedriver as uc
import yagmail
import os
import tempfile

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=SitePerProcess,IsolateOrigins,SiteIsolationTrials")
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f'--user-data-dir={user_data_dir}')
    driver = webdriver.Chrome(options=options, patcher_force_close=True)
    return driver

def human_sleep(a=1.0, b=3.0):
    time.sleep(random.uniform(a, b))

@celery_app.task
def reserve_campsite(username, password, camp_id, num_sites, start_date, end_date):
    driver = get_driver()
    try:
        # 1. Go to login page
        driver.get("https://recreation.gov")
        human_sleep(.5, 1)
        # 2. Fill in login form
        wait = WebDriverWait(driver, 20)
        # Wait for the mobile menu button to be clickable, then click it
        wait.until(EC.element_to_be_clickable((By.ID, "mobile-menu-toggle-btn"))).click()
        human_sleep(.5, 1)
        # Wait for the login link to be clickable, then click it
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sarsa-button.sarsa-button-tertiary-white.sarsa-button-md.sarsa-button-fit-container"))).click()
        human_sleep(.5, 1)
        driver.find_element(By.ID, "email").send_keys(username)
        human_sleep(.5, 1)
        driver.find_element(By.ID, "rec-acct-sign-in-password").send_keys(password)
        human_sleep(.5, 1)
        driver.find_element(By.CLASS_NAME, "rec-acct-sign-in-btn").click()
        human_sleep(.5, 1)
        # 3. Go to campground page
        driver.get(f"https://www.recreation.gov/camping/campgrounds/{camp_id}")
        human_sleep(.5, 1)
        # Select the month and start date
        start_year, start_month, start_day = start_date.split("-")
        end_year, end_month, end_day = end_date.split("-")

        month_start_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label^='month, Start Date, ']")
        month_start_div.click()
        month_start_div.send_keys(start_month)
        human_sleep(.1, .3)

        day_start_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label^='day, Start Date, ']")
        day_start_div.click()
        day_start_div.send_keys(start_day)
        human_sleep(.1, .3)

        year_start_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label^='year, Start Date, ']")
        year_start_div.click()
        year_start_div.send_keys(start_year)
        human_sleep(.1, .3)

        month_end_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label^='month, End Date, ']")
        month_end_div.click()
        month_end_div.send_keys(end_month)
        human_sleep(.1, .3)

        day_end_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label^='day, End Date, ']")
        day_end_div.click()
        day_end_div.send_keys(end_day)
        human_sleep(.1, .3)

        year_end_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label^='year, End Date, ']")
        year_end_div.click()
        year_end_div.send_keys(end_year)
        human_sleep(.5, 1)

        driver.refresh()

        human_sleep(.5, 1)

        # Get all site IDs in the tbody of the site's table
        tbody = driver.find_element(By.CSS_SELECTOR, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        site_ids = []
        for row in rows:
            site_id = row.get_attribute("id")
            if site_id:
                site_ids.append(site_id)

        sites = []
        for site_id in site_ids:
            row = driver.find_element(By.ID, site_id)
            th = row.find_element(By.TAG_NAME, "th")
            a_tag = th.find_element(By.TAG_NAME, "a")
            site_name = a_tag.text
            sites.append(site_name)

        # Traverse the sites and look for availability for the given date range
        num_sites_good = [False for site in range(0,num_sites)]
        status = "No available site found"

        # Try to find num_sites adjacent available sites for the date range
        found = False
        for idx in range(len(sites) - num_sites + 1):
            group_rows = rows[idx:idx+num_sites]
            group_sites = sites[idx:idx+num_sites]
            group_available = []
            group_start_buttons = []
            group_end_buttons = []
            for row in group_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                available = True
                start_found = False
                start_button = None
                end_button = None
                for cell in cells:
                    try:
                        button = cell.find_element(By.CSS_SELECTOR, ".rec-full-button-wrap button[aria-label]")
                        label = button.get_attribute("aria-label")
                    except Exception:
                        label = None
                    if not label:
                        continue
                    start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                    end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                    try:
                        start_label_fmt = start_dt.strftime("%b %-d, %Y")
                        end_label_fmt = end_dt.strftime("%b %-d, %Y")
                    except ValueError:
                        start_label_fmt = start_dt.strftime("%b %#d, %Y")
                        end_label_fmt = end_dt.strftime("%b %#d, %Y")
                    if start_label_fmt in label:
                        start_found = True
                        start_button = button
                    if end_label_fmt in label:
                        end_button = button
                    if start_found:
                        if "available" not in label.lower():
                            available = False
                            break
                        if end_label_fmt in label or end_date in label:
                            break
                if available and start_found and start_button and end_button:
                    group_available.append(True)
                    group_start_buttons.append(start_button)
                    group_end_buttons.append(end_button)
                else:
                    group_available.append(False)
                    break
            if len(group_available) == num_sites and all(group_available):
                # All adjacent sites are available
                for sb in group_start_buttons:
                    sb.click()
                    human_sleep(.1, .3)
                for eb in group_end_buttons:
                    eb.click()
                    human_sleep(.1, .3)
                try:
                    add_to_cart_button = driver.find_element(By.XPATH, "//button[contains(., 'Add to Cart') and not(@disabled)]")
                    add_to_cart_button.click()
                    human_sleep(.1, .3)
                    status = f"Sites {', '.join(group_sites)} added to cart for {start_date} to {end_date}"
                    found = True
                    break
                except Exception:
                    try:
                        disabled_button = driver.find_element(By.XPATH, "//button[contains(., 'Add to Cart') and @disabled]")
                    except Exception:
                        pass
                    continue
        if not found:
            human_sleep(60, 120)
        
        solver = RecaptchaSolver(driver=driver)
        recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)

        # Wait 10 seconds and check if at recreation.gov/cart
        time.sleep(30)
        if driver.current_url.startswith("https://www.recreation.gov/cart"):
            yag = yagmail.SMTP(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASSWORD"))
            yag.send(username, 
                    "Successfully reserved sites for you!", 
                    "Heya I got you some sites from your requested campground, go check your cart. You got 15 minutes."
            )
        else:
            yag = yagmail.SMTP(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASSWORD"))
            yag.send(username, 
                    "Failed to reserve sites for you!", 
                    "Heya I wasn't able to reserve the requested sites for you. Sorry about that, try again later!"
            )

    except Exception as e:
        status = f"Error: {e}"
    finally:
        driver.quit()
    return status
