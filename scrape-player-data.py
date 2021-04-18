from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from config import DRIVER_PATH, LEAGUE_ID

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

url = "https://fantasy.nfl.com/league/" + LEAGUE_ID + "/players"
driver.get(url)

# A custom expected condition class that evaluates whether
# an element's attribute equals a given value. 
class wait_for_attribute_value(object):
    def __init__(self, locator, attribute, value):
        self.locator = locator
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            element_attribute = EC._find_element(driver, self.locator).get_attribute(self.attribute)
            return element_attribute == self.value
        except StaleElementReferenceException:
            return False

# A custom expected condition class that evaluates whether
# an element has a given attribute. 
class wait_for_attribute(object):
    def __init__(self, locator, attribute):
        self.locator = locator
        self.attribute = attribute

    def __call__(self, driver):
        try:
            element_attribute = EC._find_element(driver, self.locator).get_attribute(self.attribute)
            return element_attribute != None
        except StaleElementReferenceException:
            return False

# Click to load data for all players, not just available players. 
driver.find_element_by_xpath("//select[@id='playerStatus']/option[text()='All Players']").click()
WebDriverWait(driver, 5, ignored_exceptions=(StaleElementReferenceException)).until(wait_for_attribute((By.XPATH, "//select[@id='playerStatus']/option[text()='All Players']"), "selected"))

# Click to load only receiver data. 
driver.find_element_by_id("pos3").click()
WebDriverWait(driver, 5, ignored_exceptions=(StaleElementReferenceException)).until(wait_for_attribute_value((By.XPATH, "//li[@id='pos3']"), "class", "selected"))

# Extract data from the table of players. 
html = BeautifulSoup(driver.page_source, 'html.parser')
receiversHtml = html.find_all('a', { 'class': 'playerCard' })

# Add receiver names to a list. 
receivers = []
for receiverRow in receiversHtml:
    receivers.append(receiverRow.text)

driver.quit()