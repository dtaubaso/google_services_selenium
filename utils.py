from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, requests, json, re, lxml.html, random
import undetected_chromedriver as uc

devices = ['Samsung Galaxy S20 Ultra', 'Pixel 3 XL', 'iPhone XR', 'Samsung Galaxy S8+']

# Google Questions
def getGoogleQuestions(url, clicks):
  service = Service()
  options = webdriver.ChromeOptions()
  options.add_argument("--headless=new")
  options.add_argument("--disable-gpu")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-blink-features=AutomationControlled")
  options.add_argument("--enable-javascript")
  driver = webdriver.Chrome(service=service, options=options)
  with driver:
    driver.get(url)
    try:
      for i in range(clicks):
        driver.find_elements(By.XPATH, "//div[@jsname='pcRaIe']")[i].click()
        time.sleep(0.3)
      items = driver.find_elements(By.CLASS_NAME, "CSkcDe")
      return [a.text for a in items]
    except Exception as e:
      print(e)
      return

# Tambien se buscó
def getRelated(url):
  service = Service()
  options = webdriver.ChromeOptions()
  options.add_argument("--headless=new")
  options.add_argument("--disable-gpu")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-blink-features=AutomationControlled")
  options.add_argument("--enable-javascript")
  mobile_emulation = {"deviceName": random.choice(devices)}
  print(mobile_emulation)
  options.add_experimental_option("mobileEmulation", mobile_emulation)
  driver = webdriver.Chrome(service=service, options=options)
  driver.implicitly_wait(3)
  with driver:
    try:
      driver.get(url)
      body = driver.page_source
      if body == None:
        raise Exception("Sin body")
    except Exception as e:
        print(f'Hubo un problema {e}')
        return None
  tree = lxml.html.fromstring(body)
  tambien_se_busco = tree.xpath("//div[@class='EDblX HG5ZQb']")
  element_list = [a.text_content() for a in tambien_se_busco[0].find_class("IF221e EXH1Ce")]
  related_ent = [sub.replace('\n', ' ') for sub in element_list]
  related_ent = [re.sub(' Tendencias| Tendencia| Desde.*1|Tendencia|\.\.\.Tendencia', '', a) for a in related_ent]
  related_ent = list(filter(None, related_ent))
  return related_ent

def return_body(url):
  service = Service()
  options = webdriver.ChromeOptions()
  options.add_argument("--headless=new")
  options.add_argument("--disable-gpu")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-blink-features=AutomationControlled")
  options.add_argument("--enable-javascript")
  #driver = uc.Chrome(service=service, options=options)
  driver = webdriver.Chrome(service=service, options=options)
  with driver:
    driver.get(url)
    body = driver.page_source
  return body
    



def send_slack(text, webhook_url):
  slack_data = {'text': text}
  response = requests.post(
    webhook_url, 
    data=json.dumps(slack_data), 
    headers={'Content-Type': 'application/json'}
    )