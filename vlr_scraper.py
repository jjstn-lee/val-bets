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

# find and click specific match
# TODO: find and loop through all games eventually

try:
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'col-container')]/div/div/following-sibling::div[2]"))
    )

    match_button = driver.find_element(By.XPATH, "//div[contains(@class, 'col-container')]/div/div/following-sibling::div[3]/a[1]")
    match_button.click()

except Exception as e:
    print(f"on tournament matches page and failed to click specific match: {e}")
    driver.quit()
    exit(0)



def handle_scoreboard(scoreboard):
    if (scoreboard == None) or (scoreboard.tag_name.lower() != "table"):
        print(f"WebElement passed to 'handle_scoreboard' is not a <table> element")
        return        



kda_data = pd.DataFrame(columns=["kills", "deaths", "assists", "KAST", "ADR", "ACS", "first_kills", "first_deaths"], dtype=int)

# scoreboards are all <table> elements
# find all <table> elements; the scoreboards are the 3rd and 4th table elements in DOM
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".vm-stats-game.mod-active"))
    )

    print(f"on scoreboards page")

    tables = driver.find_elements(By.CSS_SELECTOR, ".wf-table-inset.mod-overview")

    print(f"len of tables: [{len(tables)}]")

    top_scoreboard = tables[2]
    bottom_scoreboard = tables[3]

except Exception as e:
    print(f"on tournament page and failed to parse table: {e}")
    driver.quit()
    exit(0)


sleep(10)   