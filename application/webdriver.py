from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import os
from datetime import datetime as dt
from subprocess import getoutput
from pandas import read_csv


def format_csv():
    with open(getoutput('find . -name "export*"'), 'r') as file:
        try:
            data_df = read_csv(file)
            formatted_df = data_df[['active_family_size', 'family_id', 'HOH_first_name', 'HOH_last_name',
                                    'dob', 'age', 'address1', 'address2', 'zip']]
        except FileNotFoundError as e:
            return e

        return formatted_df


def login(driver):
    driver.get("https://www.pantrytrak.com")
    WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href$="login.php"]'))).click()
    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.NAME, 'username'))).send_keys(os.getenv('PANTRYTRAK_USERNAME'))
    driver.find_element(By.NAME, 'password').send_keys(os.getenv('PANTRYTRAK_PASSWORD'))
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


def get_to_check_in(driver):
    if not driver.find_element(
            by=By.XPATH,
            value='//*[contains(text(), "Church of Scientology of Ventura")]'
    ):
        login(driver)

    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.ID, 'home_form_date'))).send_keys(dt.now().strftime('%m/%d/%Y'))
    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.ID, 'search_button_alt_id'))).click()


def check_last_served(driver):
    last_served_raw = driver.find_element(By.XPATH, '//*[contains(text(), "Served Last On:")]').text
    last_served = dt.strptime(last_served_raw.split()[3], '%m/%d/%Y')
    if last_served.month == dt.now().month:
        driver.find_element(By.ID, 'form_data_4_no').click()
    else:
        driver.find_element(By.ID, 'form_data_4_yes').click()


def proxy_handler(driver, proxy):
    if proxy:
        driver.find_element(By.CSS_SELECTOR, 'option[value="proxy"]').click()
        proxy_name = proxy.split()
        proxy_initial = f"{proxy_name[0][0]}{proxy_name[1][0]}"
        proxy_signature = proxy_name.reverse().join(',')
        driver.find_element(By.CSS_SELECTOR, 'input[class="siginitials"]').send_keys(proxy_initial)
        sig_name = driver.find_element(By.CSS_SELECTOR, 'input[name="sig_name"]')
        sig_name.clear()
        sig_name.send_keys(proxy_signature)
    else:
        sig_name = driver.find_element(By.CSS_SELECTOR, 'input[name="sig_name"]').value_of_css_property('value').split()
        sig_initial = f"{sig_name[1][0]}{sig_name[0][0]}"
        driver.find_element(By.CSS_SELECTOR, 'input[class="siginitials"]').send_keys(sig_initial)


class WebDriverSingleton:

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.set_preference("browser.download.folderList", 2)
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir", '~/PycharmProjects/FoodDriveApp/tmp')
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "csv")
        self.options.binary_location = '/usr/bin/firefox'
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Firefox(options=self.options)

    def update(self, db):
        login(self.driver)
        find_report(self.driver)
        download_csv(self.driver)
        format_csv().to_sql('customer', db.engine, if_exists='replace', index=False)
        os.remove(getoutput('find . -name "export*"'))
        print(f"Finished updating database at {dt.now()}")

    def get_to_check_in(self):
        if not self.driver.find_element(
                by=By.XPATH,
                value='//*[contains(text(), "Church of Scientology of Ventura")]'
        ):
            login(self.driver)

        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.ID, 'home_form_date'))).send_keys(dt.now().strftime('%m/%d/%Y'))
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.ID, 'search_button_alt_id'))).click()

    def upload_one(self, family_id, proxy=None, provider=None):
        if self.driver.find_element(By.CSS_SELECTOR, 'div[id="search_button_alt_id"][class="search_button search_button_active"]'):
            search = self.driver.find_element(By.ID, 'omnisearch')
            search.click()
            search.send_keys(f'PTFA{family_id}')
            if provider == 'USDA':
                self.driver.find_element(By.ID, 'bgblink').click()
                check_last_served(self.driver)
                proxy_handler(self.driver, proxy)
                self.driver.find_element(By.ID, 'submitButton').click()

            else:
                self.driver.find_element(By.ID, 'radio3').click()
                self.driver.find_element(By.ID, 'status2').click()





