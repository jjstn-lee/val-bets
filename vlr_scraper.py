import re
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





# def handle_scoreboard(scoreboard):
#     if (scoreboard == None) or (scoreboard.tag_name.lower() != "table"):
#         print(f"WebElement passed to 'handle_scoreboard' is not a <table> element")
#         return
    



def handle_row(tr_element, kda_data):
    player = (tr_element.find_element(By.XPATH, "(./td)[1]/div/a/div")).text
    print(f"player: {player}")

    r20_t = float((tr_element.find_element(By.XPATH, "(./td)[3]/span/span[1]")).get_attribute("textContent"))
    r20_ct = float((tr_element.find_element(By.XPATH, "(./td)[3]/span/span[2]")).get_attribute("textContent"))
    r20_both = float((tr_element.find_element(By.XPATH, "(./td)[3]/span/span[3]")).get_attribute("textContent"))
    print(f"rating 2.0 values: {r20_t}, {r20_ct}, {r20_both}")

    acs_t = int((tr_element.find_element(By.XPATH, "(./td)[4]/span/span[2]")).get_attribute("textContent"))
    acs_ct = int((tr_element.find_element(By.XPATH, "(./td)[4]/span/span[3]")).get_attribute("textContent"))
    acs_both = int((tr_element.find_element(By.XPATH, "(./td)[4]/span/span[1]")).get_attribute("textContent"))
    print(f"acs values: {acs_t}, {acs_ct}, {acs_both}")

    kills_t = int((tr_element.find_element(By.XPATH, "(./td)[5]/span/span[2]")).get_attribute("textContent"))
    kills_ct = int((tr_element.find_element(By.XPATH, "(./td)[5]/span/span[3]")).get_attribute("textContent"))
    kills_both = int((tr_element.find_element(By.XPATH, "(./td)[5]/span/span[1]")).get_attribute("textContent"))
    print(f"kills values: {kills_t}, {kills_ct}, {kills_both}")

    deaths_both = int((tr_element.find_element(By.XPATH, "(./td)[6]/span/span[2]/span[1]")).get_attribute("textContent"))
    deaths_t = int((tr_element.find_element(By.XPATH, "(./td)[6]/span/span[2]/span[2]")).get_attribute("textContent"))
    deaths_ct = int((tr_element.find_element(By.XPATH, "(./td)[6]/span/span[2]/span[3]")).get_attribute("textContent"))
    print(f"death values: {deaths_t}, {deaths_ct}, {deaths_both}")

    assists_both = int((tr_element.find_element(By.XPATH, "(./td)[7]/span/span[1]")).get_attribute("textContent"))
    assists_t = int((tr_element.find_element(By.XPATH, "(./td)[7]/span/span[2]")).get_attribute("textContent"))
    assists_ct = int((tr_element.find_element(By.XPATH, "(./td)[7]/span/span[3]")).get_attribute("textContent"))
    print(f"assist values: {assists_t}, {assists_ct}, {assists_both}")

    kda_diff_both = int((tr_element.find_element(By.XPATH, "(./td)[8]/span/span[1]")).get_attribute("textContent"))
    kda_diff_t = int((tr_element.find_element(By.XPATH, "(./td)[8]/span/span[2]")).get_attribute("textContent"))
    kda_diff_ct = int((tr_element.find_element(By.XPATH, "(./td)[8]/span/span[3]")).get_attribute("textContent"))
    print(f"kda-diff values: {kda_diff_both}, {kda_diff_t}, {kda_diff_ct}")

    kast_both = (tr_element.find_element(By.XPATH, "(./td)[9]/span/span[1]")).get_attribute("textContent")
    kast_t = (tr_element.find_element(By.XPATH, "(./td)[9]/span/span[2]")).get_attribute("textContent")
    kast_ct = (tr_element.find_element(By.XPATH, "(./td)[9]/span/span[3]")).get_attribute("textContent")
    kast_both = float(re.sub(r'%', '', kast_both))
    kast_t = float(re.sub(r'%', '', kast_t))
    kast_ct = float(re.sub(r'%', '', kast_ct))
    print(f"kast values: {kast_both}, {kast_t}, {kast_ct}")

    adr_both = int((tr_element.find_element(By.XPATH, "(./td)[10]/span/span[1]")).get_attribute("textContent"))
    adr_t = int((tr_element.find_element(By.XPATH, "(./td)[10]/span/span[2]")).get_attribute("textContent"))
    adr_ct = int((tr_element.find_element(By.XPATH, "(./td)[10]/span/span[3]")).get_attribute("textContent"))
    print(f"adr values: {adr_both}, {adr_t}, {adr_ct}")

    hs_both = (tr_element.find_element(By.XPATH, "(./td)[11]/span/span[1]")).get_attribute("textContent")
    hs_t = (tr_element.find_element(By.XPATH, "(./td)[11]/span/span[2]")).get_attribute("textContent")
    hs_ct = (tr_element.find_element(By.XPATH, "(./td)[11]/span/span[3]")).get_attribute("textContent")
    hs_both = float(re.sub(r'%', '', hs_both))
    hs_t = float(re.sub(r'%', '', hs_t))
    hs_ct = float(re.sub(r'%', '', hs_ct))
    print(f"headshot values: {hs_both}, {hs_t}, {hs_ct}")

    fb_both = int((tr_element.find_element(By.XPATH, "(./td)[12]/span/span[1]")).get_attribute("textContent"))
    fb_t = int((tr_element.find_element(By.XPATH, "(./td)[12]/span/span[2]")).get_attribute("textContent"))
    fb_ct = int((tr_element.find_element(By.XPATH, "(./td)[12]/span/span[3]")).get_attribute("textContent"))
    print(f"first_blood values: {fb_both}, {fb_t}, {fb_ct}")

    fd_both = int((tr_element.find_element(By.XPATH, "(./td)[13]/span/span[1]")).get_attribute("textContent"))
    fd_t = int((tr_element.find_element(By.XPATH, "(./td)[13]/span/span[2]")).get_attribute("textContent"))
    fd_ct = int((tr_element.find_element(By.XPATH, "(./td)[13]/span/span[3]")).get_attribute("textContent"))
    print(f"first_death values: {fd_both}, {fd_t}, {fd_ct}")

    if player not in kda_data.index:
        kda_data.loc[player] = [kills_both, deaths_both, assists_both, kast_both, adr_both, acs_both, fb_both, fd_both]
    else:
        kda_data.at[player, "kills"] = kda_data.at[player, "kills"] + kills_both
        kda_data.at[player, "deaths"] = kda_data.at[player, "deaths"] + deaths_both
        kda_data.at[player, "assists"] = kda_data.at[player, "assists"] + assists_both
        kda_data.at[player, "KAST"] = kda_data.at[player, "KAST"] + kast_both
        kda_data.at[player, "ADR"] = kda_data.at[player, "ADR"] + adr_both
        kda_data.at[player, "ACS"] = kda_data.at[player, "ACS"] + acs_both
        kda_data.at[player, "first_kills"] = kda_data.at[player, "first_kills"] + fb_both
        kda_data.at[player, "first_deaths"] = kda_data.at[player, "first_deaths"] + fd_both
    
        
def handle_scoreboard(scoreboard, kda_data):
    # find the <tr> children (players) of scoreboard
    tr_elements = scoreboard.find_elements(By.XPATH, "./*")

    print(f"len of tr_elements: {len(tr_elements)}")

    for n in tr_elements:
        handle_row(n, kda_data)

kda_data = pd.DataFrame(columns=["kills", "deaths", "assists", "KAST", "ADR", "ACS", "first_kills", "first_deaths"], dtype=int)

def handle_match(match_button, kda_data):

    print(f"in handle_match...")

    match_button.click()

    print(f"successfully found and clicked match_button")

    WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody"))
        )
    
    print(f"successfully waited for tbody elements to load")
    
    top_scoreboard = driver.find_element(By.XPATH, "(//tbody)[3]")
    bottom_scoreboard = driver.find_element(By.XPATH, "(//tbody)[4]")

    print(f"successfully loaded scoreboards")

    handle_scoreboard(top_scoreboard, kda_data)
    handle_scoreboard(bottom_scoreboard, kda_data)

    driver.back()

try:
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'col-container')]/div/div/following-sibling::div[2]"))
    )

    # match_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-container')]/div/div/following-sibling::div[3]/a[1]")

    wf_cards = driver.find_elements(By.XPATH, '//*[@class="wf-card"]')

    print(f"len of wf_cards: {len(wf_cards)}")

    match_buttons = []

    for n in wf_cards:
        children = n.find_elements(By.XPATH, "./*")
        match_buttons.extend(children)
        print(f"len of children: {len(children)}")


    print(f"num_matches: {len(match_buttons)}")
        
    num_matches = len(match_buttons)

    for index in range(num_matches):
        # debug print
        # print(f"{n.get_attribute('href')}")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'col-container')]/div/div/following-sibling::div[2]"))
        )

        wf_cards = driver.find_elements(By.XPATH, '//*[@class="wf-card"]')

        children = []
        for n in wf_cards:
            temp = n.find_elements(By.XPATH, "./*")
            children.extend(temp)
    
        handle_match(children[index], kda_data)
        print(kda_data)

except Exception as e:
    print(f"on tournament matches page and failed to click specific match: {e}")
    driver.quit()
    exit(0)



# # scoreboards are all <table> elements
# # find all <table> elements; the scoreboards are the 3rd and 4th table elements in DOM
# try:
#     WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, ".vm-stats-game.mod-active"))
#     )

#     print(f"on scoreboards page")

#     tables = driver.find_elements(By.CSS_SELECTOR, ".wf-table-inset.mod-overview")

#     print(f"len of tables: [{len(tables)}]")

#     top_scoreboard = tables[2]
#     bottom_scoreboard = tables[3]

# except Exception as e:
#     print(f"on tournament page and failed to parse table: {e}")
#     driver.quit()
#     exit(0)

print(kda_data)

sleep(10)   