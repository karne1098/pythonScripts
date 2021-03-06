from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import re

driver = webdriver.Chrome()  # makes browser
driver.implicitly_wait(0.5)

sites = [
    "https://www.instagram.com/dogs",
    "https://www.instagram.com/frog",
]

for site in sites:
    driver.get(site)
    followers_web_elt = WebDriverWait(driver, 5, 2).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul",
            )
        )
    )
    unparsed_str = followers_web_elt.text
    # print(unparsed_str)
    unparsed_fc = re.findall("[\w|,]+ followers", unparsed_str)[0]
    fc = unparsed_fc.split(" ")[0]
    print(fc)
# print(driver.get_cookies())
driver.quit()


# NOTE code for login below
# driver.get("https://www.instagram.com/")
# sleep(3)
# driver.add_cookie({"name": "cookie", "value": "value"})
# username = driver.find_element(by=By.NAME, value="username")
# username.click()
# username.send_keys("ourstudenthandbook")
# print("user done")
# password = driver.find_element(by=By.NAME, value="password")
# print("password done")
# password.send_keys("qpalzm1098")
# password.send_keys(Keys.RETURN)

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located(
#         (By.XPATH, "/html/body/div[1]/section/main/div/div")
#     )
# )

# /html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div
# #/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/ul/li[2]/a/div
# <div class="_aacl _aacp _aacu _aacx _aad6 _aade"><span class="_ac2a" title="810,046">810K</span> followers</div>
# <div class="_aacl _aacp _aacu _aacx _aad6 _aade"><span class="_ac2a" title="25,628">25.6K</span> followers</div>
