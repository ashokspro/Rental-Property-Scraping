import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time

URL = "https://appbrewery.github.io/Zillow-Clone/"
webpage = requests.get(URL)

soup = BeautifulSoup(webpage.content, "html.parser")
address_tag = soup.find_all("address")
address = []
for add in address_tag:
    address.append(add.getText(strip=True))

link_tag = soup.find_all("a", {"data-test": "property-card-link"})
links = []
for lin in link_tag:
    links.append(lin.get("href"))

links = list(set(links))
price_tag = soup.find_all("span", {"data-test": "property-card-price"})
price_with_cases = []
for p in price_tag:
    price_with_cases.append(p.getText(strip=True))


pattern = r"\$([\d,]+)"
prices = [re.sub(r',', '', match.group()) for price in price_with_cases for match in [re.search(pattern, price)] if match]

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://forms.gle/Gz71n2JXjERw5m7A9")
time.sleep(3)

for data in range(len(address)+1):
    try:
        address_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/textarea')
        address_input.send_keys(address[data])
        price_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/textarea')
        price_input.send_keys(prices[data])
        link_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[2]/textarea')
        link_input.send_keys(links[data])
        submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
        submit_button.click()
        another_response = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        another_response.click()
    except IndexError:
        print("The Data submitted successfully")