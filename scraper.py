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

# find and click on a particular match
try:
    matches = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.table-cell.c-global-match-link"))
    )

    print("Found match link:", matches.get_attribute("href"))
    print("Found match link:", matches.get_attribute("class"))
    print("Tag name:", matches.tag_name)  # Should print 'a'

    driver.execute_script("arguments[0].scrollIntoView(true);", matches)
    driver.execute_script("arguments[0].click();", matches)

except Exception as e:
    print(f"failed to handle all matches button: {e}")
    driver.quit()
    exit(0)

player_data = pd.DataFrame(columns=["kills", "deaths", "assists"], dtype=int)

# need to make sure to navigate back
# for a given match, populate player_data with the proper stats
def handle_finished_match():

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

        print(f"len of top_rows: {len(top_rows)}")
        print(f"len of bottom_rows: {len(bottom_rows)}")

        for row in top_rows:
            handle_row(row)

        for row in bottom_rows:
            handle_row(row)





    except Exception as e:
        print(f"finding player and stats went wrong: {e}")    
        print(player_data)
        driver.quit()
        exit(0)


# take a row and find the player and their corresponding kda
# insert the information into pandas dataframe
# row is a WebElement
def handle_row(row):
    global player_data

    # find player name and convert it to a string
    name = (row.find_element(By.XPATH, "./div/div/a/span[2]")).text

    # first find wrapper for kills/deaths/assists; then find deaths and assists based on location of wrapper class
    kda = row.find_element(By.XPATH, "./div/following-sibling::div[2]")

    kills = kda.find_element(By.XPATH, "./div[1]/p")
    deaths = kda.find_element(By.XPATH, "./div[2]/p")
    assists =  kda.find_element(By.XPATH, "./div[3]/p")

    kills = int(kills.text)
    deaths = int(deaths.text)
    assists = int(assists.text)

    print(f"  player_name: {name}")
    print(f"  kills: {kills}, type: {type(kills)}")
    print(f"  deaths: {deaths}, type: {type(deaths)}")
    print(f"  assists: {assists}, type: {type(assists)}")

    if name not in player_data.index:
        player_data.loc[name] = [kills, deaths, assists]
    else:
        print(f"Before update: {player_data.loc[name]}")  # Debug line
        player_data.loc[name, "kills"] += kills
        player_data.loc[name, "deaths"] += deaths
        player_data.loc[name, "assists"] += assists
        print(f"After update: {player_data.loc[name]}")  # Debug line

handle_finished_match()

print(player_data)

sleep(10)

