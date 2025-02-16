from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd

driver = webdriver.Chrome()
driver.get("https://bo3.gg/valorant")


# wait for website to load
try:
    WebDriverWait(driver, 20).until(
        EC.title_contains("Valorant")
    )
except Exception as e:
    print(f"failed to load initial page: {e}")
    driver.quit()

# wait for spoilers pop up and close it
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".vfm__content.vfm--outline-none"))
    )

    # find spoiler pop-up button based on position in DOM
    buttons = driver.find_elements(By.CSS_SELECTOR, ".c-button.c-button--full-width")
    spoilers_button = buttons[5]

    # use javascript click
    driver.execute_script("arguments[0].click();", spoilers_button)
except Exception as e:
    print(f"failed to handle spoiler pop-up: {e}")
    driver.quit()
    exit(0)

# click "tournaments" button
# bce we waited for pop-up first, button should be loaded by now
try:
    print(f"looking for matches button...")

    tournaments_button = driver.find_element(By.LINK_TEXT, "Tournaments")
    print(f"clicking tournaments button...")
    tournaments_button.click()
except Exception as e:
    print(f"failed to click matches or finished button: {e}")
    driver.quit()

# wait for "finished" button and click it
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Finished"))
    )

    finished_button = driver.find_element(By.LINK_TEXT, "Finished")
    print(f"clicking finished button...")
    finished_button.click()

except Exception as e:
    print(f"failed to handle finish button: {e}")
    driver.quit()
    exit(0)

# find and click button for VCT 2025: Americas Kickoff
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table-cell.event.c-table-cell-tournament.event--finished")) # css classes for tournaments
    )

    tournaments = driver.find_elements(By.CSS_SELECTOR, ".table-cell.event.c-table-cell-tournament.event--finished")
    
    kickoff_button = tournaments[2]
    kickoff_button.click()

except Exception as e:
    print(f"failed to click on kickoffs button: {e}")
    driver.quit()
    exit(0)

# find and click "results" button
try:
    print(f"waiting for all matches button to be clickable")
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Results"))
    ).click()
except Exception as e:
    print(f"failed to handle all matches button: {e}")
    driver.quit()
    exit(0)

try:
    matches = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.table-cell.c-global-match-link"))
    )

    print("Found match link:", matches.get_attribute("href"))
    print("Found match link:", matches.get_attribute("class"))
    print("Tag name:", matches.tag_name)  # Should print 'a'

    driver.execute_script("arguments[0].scrollIntoView(true);", matches)
    driver.execute_script("arguments[0].click();", matches)

    print("i'm here! :)")
except Exception as e:
    print(f"failed to handle all matches button: {e}")
    driver.quit()
    exit(0)


df = pd.DataFrame()

# need to make sure to navigate back
# def handle_match() {

# }



sleep(10)

