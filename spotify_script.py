from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


sites = [
    "https://open.spotify.com/artist/2DDdkJNNuomH4Px5AJ8p2d?si=XxmUd8q1Thi4SewNo-u4Mw",
    "https://open.spotify.com/artist/39FKVjqhZLz4E1iG77d5AO?si=9F2ec-ZxRsqIai4BLkc9KQ",
    "https://open.spotify.com/artist/01Kz5ab1oYMaey58CaGTxA?si=eEphvNjoT_WuHIiZhQbGXA",
    "https://open.spotify.com/artist/2eV1QNmQNiCO6cqCYhFES1?si=QguMRfZKSsareFjqReYzdw",
    "https://open.spotify.com/artist/53WX2PlTCRBDSlePgc6v5C?si=IanHtaACSHqanXKN1MZvuw",
    "https://open.spotify.com/artist/5CgifoNp4VZAgyQmiXPv7N?si=VaUx4kP_S1aRI1XsD3YfnA",
    "https://open.spotify.com/artist/1tzZtJUaD3xPSetRFaP5Ae?si=mmYxUS-ARoyEqjWYiBCvoA",
    "https://open.spotify.com/artist/2WZrsTVfrVptqmu3cPtv2C?si=TmlUiABvTKSsfe8PUs_KLw",
    "https://open.spotify.com/artist/0XJA8RpM6VgQeIYzjnP8wK?si=F0SPwfjCT1mjNhEy7Wf3sw",
]

driver = webdriver.Chrome()  # makes browser
driver.implicitly_wait(0.5)


# def pee(driver):
#     return driver.find_element(  # gets the web element w subscriber count
#         by=By.CSS_SELECTOR,
#         value="#main > div > div.Root__top-container > div.Root__main-view > div.main-view-container > div.os-host.os-host-foreign.os-theme-spotify.os-host-resize-disabled.os-host-scrollbar-horizontal-hidden.main-view-container__scroll-node.os-host-transition.os-host-overflow.os-host-overflow-y > div.os-padding > div > div > div.main-view-container__scroll-node-child > main > section > div > div.contentSpacing.NXiYChVp4Oydfxd7rT5r.RMDSGDMFrx8eXHpFphqG > div.RP2rRchy4i8TIp1CTmb7 > span.Ydwa1P5GkCggtLlSvphs",
#     )


for site in sites:
    driver.get(site)
    try:
        followers_web_elt = WebDriverWait(driver, 3, 1.5).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[3]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[1]",
                )
                # "/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[1]"
            )  # melv "/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[1]/div[5]"
        )
        unparsed_str = followers_web_elt.text
        # print(unparsed_str)
        unparsed_fc = re.findall("[\w|,]+ monthly listeners", unparsed_str)[0]
        fc = unparsed_fc.split(" ")[0]
        print(fc)
    except:
        try:
            followers_web_elt = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[1]",
                    )
                )
            )
            unparsed_str = followers_web_elt.text
            unparsed_fc = re.findall("[\w|,]+ monthly listeners", unparsed_str)[0]
            fc = unparsed_fc.split(" ")[0]
            print(fc)
        except:
            print("ugh")


driver.quit()
