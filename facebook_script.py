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
    "https://www.facebook.com/MICHELLE-299893597455645/",
    "https://facebook.com/carolinepolachekmusic",
    "https://www.facebook.com/alicephoebeloumusic/",
]

follower_counts = []
for site in site_ls:
    driver.get(site)
    sleep(3)
    try:
        followers_web_elt = driver.find_element(  # gets the web element w subscriber count
            by=By.XPATH,
            value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span",
        )
    except:
        followers_web_elt = driver.find_element(  # gets the web element w subscriber count
            by=By.XPATH,
            value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div/div[2]/div/div/span/span",
        )

    # //*[@id="mount_0_0_8F"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span
    #
    # /html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span
    follower_count = followers_web_elt.text.split(" ")[0]
    follower_counts.append(follower_count)
print(follower_counts)
# print(driver.get_cookies())
driver.quit()
