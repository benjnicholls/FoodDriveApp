from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime


def login(driver):
    driver.get("https://www.pantrytrak.com")
    WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href$="login.php"]'))).click()
    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.NAME, 'username'))).send_keys("mgr-cos")
    driver.find_element(By.NAME, 'password').send_keys("mgr-pa0580")
    driver.find_element(By.NAME, 'submit').click()
    print("Logged in")


def find_report(driver):
    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.NAME, 'sig_name'))).send_keys("Benjamin Nicholls")
    driver.find_element(By.NAME, 'sig_initials').send_keys("BN")
    driver.find_element(By.XPATH, '//*[contains(text(), "I Understand")]').click()
    print("Authorization verified.")
    WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Analysis & Learning Center")]'))).click()
    print('Entered Reports page')
    driver.find_element(By.ID, 'tipid20').click()
    print('Entered family report')
    driver.switch_to.window(driver.window_handles[1])


def download_csv(driver):
    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.ID, 'start_date'))).send_keys("04/01/2023")
    driver.find_element(By.ID, 'end_date').send_keys(str(datetime.now().strftime("%m/%d/%Y")))
    driver.find_element(By.CSS_SELECTOR, 'input[value="csv"]').click()
    driver.find_element(By.NAME, 'submit').click()
    print("Downloading CSV")


class WebDriverSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.set_preference("browser.download.folderList", 2)
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir", '~/PycharmProjects/FoodDriveApp/resources')
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "csv")
        self.options.binary = FirefoxBinary('/lib/firefox/firefox.sh')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Firefox(options=self.options)

    def close(self):
        self.driver.close()

    def update(self):
        login(self.driver)
        find_report(self.driver)
        download_csv(self.driver)
        print("Terminating bot")
        self.driver.close()

    def upload(self):
        login(self.driver)
