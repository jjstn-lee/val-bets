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

    # find spoiler pop-up button and click first option
    buttons = driver.find_elements(By.CSS_SELECTOR, ".c-button.c-button--full-width")
    spoilers_button = buttons[5]
    driver.execute_script("arguments[0].click();", spoilers_button)
except Exception as e:
    print(f"failed to handle spoiler pop-up: {e}")
    driver.quit()
    exit(0)

# click "tournaments" button
try:
    print("finding and clicking tournaments button...")
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Tournaments"))
    ).click()
except Exception as e:
    print(f"failed to click tournaments button: {e}")
    driver.quit()

# wait for "finished" button and click it
try:
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Finished"))
    ).click()
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

kda_data = pd.DataFrame(columns=["kills", "deaths", "assists"], dtype=int)

# need to make sure to navigate back
# for a given match, populate kda_data with the proper stats
def handle_finished_match(match):
    # scroll to match and click it
    driver.execute_script("arguments[0].scrollIntoView(true);", match)
    driver.execute_script("arguments[0].click();", match)

    print(f"Clicked on match: {match}")

    print(f"waiting for table to load...")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".o-widget.c-widget-match-scoreboard"))
    )

    print(f"table loaded, finding <> w/ .nickname...")
    try:
        # find entire scoreboard
        scoreboards = driver.find_elements(By.XPATH, "//div[contains(text(), 'Scoreboard')]/following-sibling::div/div/div/div/following-sibling::div")
        
        # separate scoreboards into top and bottom teams
        top_team = scoreboards[0]
        bottom_team = scoreboards[1]

        # find important rows in the scoreboard
        top_rows = top_team.find_elements(By.XPATH, "./div[contains(@class, 'table-row') and not(contains(@class, 'total'))]")
        bottom_rows = bottom_team.find_elements(By.XPATH, "./div[contains(@class, 'table-row') and not(contains(@class, 'total'))]")

        # print(f"len of top_rows: {len(top_rows)}")
        # print(f"len of bottom_rows: {len(bottom_rows)}")

        # process rows
        for row in top_rows:
            handle_row(row)

        for row in bottom_rows:
            handle_row(row)

        driver.back()
    except Exception as e:
        print(f"finding player and stats went wrong: {e}")    
        print(kda_data)
        driver.quit()
        exit(0)


# take a row and find the player and their corresponding kda
# insert the information into pandas dataframe
# row is a WebElement
def handle_row(row):
    try:
        global kda_data

        # find player name and convert it to a string
        name = (row.find_element(By.XPATH, "./div/div/a/span[2]")).text

        # first find wrapper for kills/deaths/assists; then find kills, deaths, and assists based on location of wrapper class
        kda = row.find_element(By.XPATH, "./div/following-sibling::div[2]")

        kills = kda.find_element(By.XPATH, "./div[1]/p")
        deaths = kda.find_element(By.XPATH, "./div[2]/p")
        assists =  kda.find_element(By.XPATH, "./div[3]/p")

        kills = int(kills.text)
        deaths = int(deaths.text)
        assists = int(assists.text)

        if name not in kda_data.index:
            kda_data.loc[name] = [kills, deaths, assists]
        else:
            kda_data.at[name, "kills"] = kda_data.at[name, "kills"] + kills
            kda_data.at[name, "deaths"] = kda_data.at[name, "deaths"] + deaths
            kda_data.at[name, "assists"] = kda_data.at[name, "assists"] + assists
    except Exception as e:
        print(f"error in handle_row: {e}")
        driver.quit()
        exit(0)

# find and handle all matches
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.table-cell.c-global-match-link"))
    )

    matches = driver.find_elements(By.CSS_SELECTOR, "a.table-cell.c-global-match-link")
    num_matches = len(matches)

    for n in range(num_matches):
        # find these again just in case the page changes
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.table-cell.c-global-match-link"))
        )
        matches = driver.find_elements(By.CSS_SELECTOR, "a.table-cell.c-global-match-link")

        # just in case the results page shows the academy teams instead
        while num_matches != len(matches):
            print(f"num_matches ({num_matches}) != len(matches) {len(matches)}")
            driver.refresh()
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.table-cell.c-global-match-link"))
            )
            matches = driver.find_elements(By.CSS_SELECTOR, "a.table-cell.c-global-match-link")  

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(matches[n])
        )
        handle_finished_match(matches[n])
        print(f"count: {n}")
        print(kda_data)

    sleep(50)
except Exception as e:
    print(f"error here!!: {e}")
    print(kda_data)
    driver.quit()
    exit(0)

print(kda_data)

kda_data.to_csv('kda_data.txt', index="True", sep=' ')

sleep(10)