from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

driver = webdriver.Chrome()  # makes browser
driver.implicitly_wait(0.5)

site_ls = [
    "https://www.facebook.com/UNIIQU3MUSIC",
    "https://www.facebook.com/MIKEDIMESORMKEDEEZY/",
    "https://www.facebook.com/JoshWatersMusic/",
    "https://www.facebook.com/batheboys/",
    "https://www.facebook.com/kurtisrwells/",
    "https://www.facebook.com/bleachlab/",
    "https://www.facebook.com/MontellFish",
    "https://www.facebook.com/jexnwalor/",
    "https://www.facebook.com/Moliymusic",
    "https://www.facebook.com/1NF1N1T3C0L35/",
    "https://www.facebook.com/withachanceofrain",
    "https://www.facebook.com/emelineisme/",
]


def parse_count(text_number):
    tens = {"K": 1000, "M": 1000000}
    text_number = text_number.upper()
    if (text_number[-1] == "K") or (text_number[-1] == "M"):
        return int(float(text_number[:-1]) * tens[text_number[-1]])
    else:
        if "," in text_number:
            text_number = text_number.replace(",", "")
        return int(text_number)


for site in site_ls:
    driver.get(site)
    try:
        followers_web_elt = (
            driver.find_element(  # gets the web element w subscriber count
                by=By.PARTIAL_LINK_TEXT, value="followers"
            )
        )
        parsed = parse_count(followers_web_elt.text.split(" ")[0])
        print(parsed)
    except:
        try:
            followers_web_elt = (
                driver.find_element(  # gets the web element w subscriber count
                    by=By.PARTIAL_LINK_TEXT, value="likes"
                )
            )
            parsed = parse_count(followers_web_elt.text.split(" ")[0])
            print(parsed)
        except:
            try:
                followers_web_elt = driver.find_element(  # gets the web element w subscriber count
                    by=By.XPATH,
                    value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[1]",
                )
                parsed = parse_count(followers_web_elt.text.split(" ")[0])
                print(parsed)
            except:

                try:
                    followers_web_elt = driver.find_element(  # gets the web element w subscriber count
                        by=By.XPATH,
                        value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div",
                    )
                    unparsed_str = followers_web_elt.text
                    unparsed_fc = re.findall(
                        "[\w|,]+ people follow this", unparsed_str
                    )[0]
                    fc = parse_count(unparsed_fc.split(" ")[0])
                    print(fc)
                except:
                    print("unsucessful " + site)

# follower_counts = []
# for site in site_ls:
#     driver.get(site)
#     try:
#         followers_web_elt = (
#             driver.find_element(  # gets the web element w subscriber count
#                 by=By.PARTIAL_LINK_TEXT, value="followers"
#             )
#         )
#         unparsed = followers_web_elt.text.split(" ")[0]
#         fc = parse_count(unparsed)

#     except:
#         try:
#             followers_web_elt = driver.find_element(  # gets the web element w subscriber count
#                 by=By.XPATH,
#                 value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div/div[2]/div/div/span/span",
#             )  # "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div/div[2]/div/div/span"
#             # "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div"
#             # "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div"
#             fc = parse_count((followers_web_elt.text.split(" ")[0]))
#         except:
#             try:
#                 followers_web_elt = driver.find_element(  # gets the web element w subscriber count
#                     by=By.XPATH,
#                     value="/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[2]/div",
#                 )
#                 fc = parse_count(followers_web_elt.text.split(" ")[0])
#             except:
#                 try:
#                     followers_web_elt = driver.find_element(  # gets the web element w subscriber count
#                         by=By.XPATH,
#                         value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div/div[2]/div/div/span/span",
#                     )
#                     fc = parse_count(followers_web_elt.text.split(" ")[0])
#                 except:
#                     fc = "manual"

# //*[@id="mount_0_0_8F"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span
#
# /html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span

# print(follower_counts)
# print(driver.get_cookies())
driver.quit()
