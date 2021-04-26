import json
import numpy as np
from sklearn.linear_model import LinearRegression
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import DRIVER_PATH

def to_js(output):
  print(json.dumps(output))

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

def run_regression(x, y):
  x = np.array(x).reshape((-1, 1)).astype(np.float64)
  y = np.array(y).astype(np.float64)

  model = LinearRegression()
  model.fit(x, y)

  intercept  = model.intercept_
  coef = model.coef_[0]
  R_sq = model.score(x, y)

  return (intercept, coef, R_sq)

# Parses text into a numeric value, returning 
# 0 for missing data. 
def parseFloat(string):
  try:
      return float(string)
  except ValueError:
      return 0