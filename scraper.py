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

except Exception as e:
    print(f"failed to handle all matches button: {e}")
    driver.quit()
    exit(0)


player_data = pd.DataFrame()

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
        
        # for s in scoreboards:
        #     print(s.text)
        #     print(s.get_attribute("value"))

        
        top_team = scoreboards[0]
        bottom_team = scoreboards[1]

        top_rows = top_team.find_elements(By.CSS_SELECTOR, ".table-cell.player")

        for players in top_rows:
            print(players.get_attribute("value"))


        # print(top_team.text)
        # print(bottom_team.text)



        
        
        players = driver.find_elements(By.CLASS_NAME, "nickname")
        
        player_names = {}

        for n in players:
            player_names[n.text] = [0, 0, 0]
        print(player_names)

    except Exception as e:
        print(f"finding player and stats went wrong: {e}")    
        print(player_data)
        driver.quit()
        exit(0)


handle_finished_match()

sleep(10)

