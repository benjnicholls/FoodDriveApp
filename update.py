from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import date


def webdriver_step():
    options = Options()
    # options.add_argument('--headless')
    options.binary = FirefoxBinary('/lib/firefox/firefox.sh')
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", '~/PycharmProjects/FoodDriveApp/resources')
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "csv")
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Firefox(options=options)
    driver.get("https://www.pantrytrak.com")
    assert "FreshTrak" in driver.title
    driver.find_element(By.XPATH, '//*[contains(text(), "Login")]').click()
    driver.find_element(By.NAME, 'username').send_keys("mgr-cos")
    driver.find_element(By.NAME, 'password').send_keys("mgr-pa0580")
    driver.find_element(By.NAME, 'submit').click()
    print("Logged in")

    driver.find_element(By.NAME, 'sig_name').send_keys("BENJAMIN NICHOLLS")
    driver.find_element(By.NAME, 'sig_initials').send_keys("BN")
    driver.find_element(By.XPATH, '//*[contains(text(), "I Understand")]').click()
    print("Authorization verified.")
    driver.find_element(By.XPATH, '//*[contains(text(), "Analysis & Learning Center")]').click()
    print('Entered Reports page')
    driver.find_element(By.ID, 'tipid20').click()
    print('Entered family report')

    driver.switch_to.window(driver.window_handles[1])
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'start_date')))

    driver.find_element(By.ID, 'start_date').send_keys("04/01/2023")
    driver.find_element(By.ID, 'end_date').send_keys(str(date.today().strftime("%m/%d/%Y")))
    driver.find_element(By.CSS_SELECTOR, 'input[value="csv"]').click()
    driver.find_element(By.NAME, 'submit').click()
    print("Downloading CSV")
    print("Terminating bot")
    driver.quit()
    

webdriver_step()
