from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, requests, json, re
import chromedriver_binary


# Google Questions
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

# Tambien se buscó
def getRelated(url):
  options = webdriver.ChromeOptions()
  options.add_argument("--headless")
  options.add_argument("--disable-gpu")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(options=options)
  driver.implicitly_wait(3)
  with driver:
    driver.get(url)
    x_path = "//*[text()='Otras personas también buscan' or text()='También se buscó']"
    x_path_link = "//*[text()='Otras personas también buscan' or text()='También se buscó' or text()='Ver más']"
    try:
        # mbappe
        if driver.find_elements(By.CLASS_NAME,"TzHB6b"):
          link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Ver más")))
          link.click()
        elif driver.find_elements(By.CLASS_NAME,"liYKde"):
          link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, x_path)))
          link.click()
        time.sleep(2)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'ct5Ked')))
        elements = driver.find_elements(By.CLASS_NAME,"ct5Ked")
        element_list = [x.text for x in elements]
        related_ent = [sub.replace('\n', ' ') for sub in element_list]
        related_ent = [re.sub(' Tendencias| Tendencia| Desde.*', '', a) for a in related_ent]
        related_ent = list(filter(None, related_ent))
        return related_ent
    except Exception as e:
        print(f'Hubo un problema {e}')



def send_slack(text, webhook_url):
  slack_data = {'text': text}
  response = requests.post(
    webhook_url, 
    data=json.dumps(slack_data), 
    headers={'Content-Type': 'application/json'}
    )