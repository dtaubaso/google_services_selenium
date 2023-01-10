from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

def getGoogleQuestions(url, clicks):
  options = webdriver.ChromeOptions()
  options.add_argument("--headless")
  options.add_argument("--disable-gpu")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(options=options)
  with driver:
    driver.get(url)
    try:
      for a in range(clicks):
        driver.find_elements(By.XPATH, "//div[@jsname='F79BRe']")[a].click()
        time.sleep(0.3)
      items = driver.find_elements(By.XPATH, "//div[@jsname='jIA8B']")
      return [a.text for a in items]
    except Exception as e:
      print(e)
      return