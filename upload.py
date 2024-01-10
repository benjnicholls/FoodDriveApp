from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from subprocess import getoutput
from selenium.webdriver.firefox.service import Service

options = webdriver.FirefoxOptions()
options.binary = FirefoxBinary(getoutput('~/usr/bin/firefox'))
service = Service(executable_path='~/Downloads/geckodriver.exe')

driver = webdriver.Firefox(options=options)
driver.get("https://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()