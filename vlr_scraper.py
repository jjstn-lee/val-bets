from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd

driver = webdriver.Chrome()
driver.get("https://www.vlr.gg/")

# wait for website to load
try: 
    WebDriverWait(driver, 20).until(
        EC.title_contains("Valorant")
    )
except Exception as e:
    print(f"failed to load initial page")
    driver.quit()
    exit(0)

# find and click 'Events' button
try:
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Events"))
    ).click()
except Exception as e:
    print(f"failed to click 'Events' button: {e}")
    driver.quit()
    exit(0)

# find and click 'North America' button
try:
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "North America"))
    ).click()
except Exception as e:
    print(f"failed to click 'Events' button: {e}")
    driver.quit()
    exit(0)

# find and click 'Champions Tour 2025: Americas Kickoff"
try:
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Champions Tour 2025: Americas Kickoff"))
    ).click()
except Exception as e:
    print(f"failed to click 'Champions Tour 2025: Americas Kickoff' button: {e}")
    driver.quit()
    exit(0)

# find and click proper 'Matches' button based on navbar position in DOM
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "wf-nav"))
    )
    navbar = driver.find_element(By.CLASS_NAME, "wf-nav")
    matches_button = navbar.find_element(By.XPATH, "./a[2]")
    matches_button.click()
except Exception as e:
    print(f"on tournament page and failed to click 'matches' button: {e}")
    driver.quit()
    exit(0)


# TODO: find and loop through all games





kda_data = pd.DataFrame(columns=["kills", "deaths", "assists", "KAST", "ADR", "ACS", "first_kills", "first_deaths"], dtype=int)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".vm-stats-game.mod-active"))
    )

    scoreboard = driver.find_element(By.CLASS_NAME, "vm-stats-container")

    top_scoreboard = scoreboard.find_element(By.XPATH, "./div/following-sibling::div[1]")
    bottom_scoreboard = scoreboard.find_element(By.XPATH, "./div/following-sibling::div[2]")





except Exception as e:
    print(f"on tournament page and failed to parse table: {e}")
    driver.quit()
    exit(0)


sleep(10)   