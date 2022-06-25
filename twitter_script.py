from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path
import numpy as np
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()  # makes browser
driver.implicitly_wait(0.5)

site_ls = [
    "https://twitter.com/michelletheband",
    "https://twitter.com/carolineplz",
    "https://twitter.com/alicephoebelou",
]

follower_counts = []
for site in site_ls:
    driver.get(site)
    sleep(3)
    try:
        followers_web_elt = driver.find_element(  # gets the web element w subscriber count
            by=By.XPATH,
            value="/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[5]/div[2]/a/span[1]/span",
        )  # /html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[4]/div[2]/a/span[1]/span
    except:
        followers_web_elt = driver.find_element(  # gets the web element w subscriber count
            by=By.XPATH,
            value="/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[4]/div[2]/a/span[1]/span",
        )

    follower_count = followers_web_elt.text
    follower_counts.append(follower_count)
print(follower_counts)
# print(driver.get_cookies())
driver.quit()
