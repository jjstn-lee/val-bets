from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://bo3.gg/valorant")

try:
    WebDriverWait(driver, 20).until(EC.title_contains("Valorant"))
except:
    print("failed to load initial page, quitting...\n")
    driver.quit()

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(By.CLASS_NAME, "vfm__content vfm--outline-none")
    )

    # need driver to click "spoilers" button next

except:
    print("failed to load spoiler pop-up")


# assert "bo3" in driver.title
# assert "valorant" in driver.title 

try:
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "/valorant/matches/")
    ))

    matches = driver.find_elements(By.PARTIAL_LINK_TEXT, "/valorant/matches/")
    print("successfully loaded table, locating matc hes...")

    print(f"len of matches: {len(matches)}")
    for n in range(len(matches)):
        print(matches[n].text)

except:
    print("failed to fetch table, quitting...\n")
    driver.quit()


