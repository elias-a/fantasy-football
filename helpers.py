from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import DRIVER_PATH

def scrape(url, filename):
  options = Options()
  options.headless = True

  driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

  driver.get(url)

  with open(filename, 'w') as f:
    f.write(driver.page_source)

  driver.quit()

def format_name(name):
  return "".join([c for c in name if c.isupper()])