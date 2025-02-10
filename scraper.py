from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://bo3.gg/valorant")

try:
    WebDriverWait(driver, 20).until(
        EC.title_contains("Valorant")
    )
except Exception as e:
    print(f"failed to load initial page: {e}")
    driver.quit()    

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


# assert "bo3" in driver.title
# assert "valorant" in driver.title 



# wait for pop-up first, so matches button should be loaded by now
try:
    print(f"looking for matches button...")

    tournaments_button = driver.find_element(By.LINK_TEXT, "Tournaments")
    print(f"clicking tournaments button...")
    tournaments_button.click()
    # finished_button = driver.find_element(By.LINK_TEXT, "Finished")
    # print(f"clicking finished button...")
    # finished_button.click()

except Exception as e:
    print(f"failed to click matches or finished button: {e}")
    driver.quit()

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Finished"))
    )

    finished_button = driver.find_element(By.LINK_TEXT, "Finished")
    finished_button.click()

except Exception as e:
    print(f"failed to handle finish button: {e}")
    driver.quit()
    exit(0)


sleep(10)