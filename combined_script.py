import string
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path
import numpy as np
from time import sleep

driver = webdriver.Chrome()  # makes browser
driver.implicitly_wait(0.5)
titles = ["artist name", "tiktok", "instagram", "twitter", "facebook", "youtube"]


def make_data_array(data_file):
    training = Path(data_file)
    dataframe = pd.read_csv(
        training,
        sep=",",
        delimiter=None,
        header="infer",
        names=None,
        index_col=None,
        usecols=titles,
        squeeze=False,
        prefix=None,
        mangle_dupe_cols=True,
        dtype=None,
        engine=None,
        converters=None,
        true_values=None,
        false_values=None,
        skipinitialspace=False,
        skiprows=None,
        skipfooter=0,
        nrows=None,
        na_values=None,
        keep_default_na=True,
        na_filter=True,
        verbose=False,
        skip_blank_lines=False,
        parse_dates=False,
        infer_datetime_format=False,
        keep_date_col=False,
        date_parser=None,
        dayfirst=False,
        cache_dates=True,
        iterator=False,
        chunksize=None,
        compression="infer",
        thousands=None,
        decimal=".",
        lineterminator=None,
        quotechar='"',
        quoting=0,
        doublequote=True,
        escapechar=None,
        comment=None,
        encoding=None,
        encoding_errors="strict",
        dialect=None,
        error_bad_lines=None,
        warn_bad_lines=None,
        on_bad_lines=None,
        delim_whitespace=False,
        low_memory=True,
        memory_map=False,
        float_precision=None,
        storage_options=None,
    )

    data = dataframe.to_numpy()
    # XXX print(len(youtube_sites))
    return data


"""
test = make_data_array("eq subset.csv")
print(test)
artists = test[:, 0]
tiktoks = test[:, 1]
print(artists)
print(tiktoks)
print(test)

"""


# function to keep 200 as 200 and change 1.7k --> 1,700 and 16.2m --> 16,200,000
def parse_count(text_number):
    tens = {"K": 1000, "M": 1000000}
    text_number = text_number.upper()
    if (text_number[-1] == "K") or (text_number[-1] == "M"):
        return int(float(text_number[:-1]) * tens[text_number[-1]])
    else:
        if "," in text_number:
            text_number = text_number.replace(",", "")
        return int(text_number)


def tiktok_fc():
    followers_web_elt = driver.find_element(  # gets the web element w subscriber count
        by=By.XPATH,
        value="/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[2]/strong",
    )
    follower_count = parse_count(followers_web_elt.text)
    return follower_count


def twitter_fc():
    sleep(1)
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
    fc = parse_count(followers_web_elt.text)
    return fc


def facebook_fc():
    sleep(1)
    try:
        followers_web_elt = driver.find_element(  # gets the web element w subscriber count
            by=By.XPATH,
            value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span",
        )
    except:
        try:
            followers_web_elt = driver.find_element(  # gets the web element w subscriber count
                by=By.XPATH,
                value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div/div[2]/div/div/span/span",
            )
        except:
            try:
                followers_web_elt = driver.find_element(  # gets the web element w subscriber count
                    by=By.XPATH,
                    value="/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[2]/div",
                )
            except:
                followers_web_elt = driver.find_element(  # gets the web element w subscriber count
                    by=By.XPATH,
                    value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div/div[2]/div/div/span/span",
                )

    fc_unparsed = followers_web_elt.text.split(" ")[0]
    fc = parse_count(fc_unparsed)
    return fc


def youtube_fc():
    try:
        followers_web_elt = driver.find_element(  # gets the web element w subscriber count
            by=By.XPATH,
            value="/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/yt-formatted-string",
        )
        fc_unparsed = followers_web_elt.text.split(" ")[0]  # parses subscriber count
        fc = parse_count(fc_unparsed)
    except:
        fc = ""
    return fc


def fill_one_fc(social_media, site_array):

    follower_counts = []
    if social_media == "instagram":
        follower_counts = [""] * len(site_array)
    else:
        for site in site_array:
            if pd.isna(site):
                follower_counts.append("")
            else:
                driver.get(site)
                follower_count = eval(social_media + "_fc()")
                follower_counts.append(follower_count)
    return follower_counts


"""
    if social_media == "tiktok":
        for site in site_array:  # populates follower_counts
            if pd.isna(site):
                follower_counts.append("")
            else:
                driver.get(site)
                follower_count = tiktok_fc(driver)
                follower_counts.append(follower_count)
    elif social_media == "instagram":
        follower_counts = [""] * len(site_array)
    elif social_media == "twiter":
        for site in site_array:  # populates follower_counts
            if pd.isna(site):
                follower_counts.append("")
            else:
                driver.get(site)
                follower_count = twitter_fc(driver)
                follower_counts.append(follower_count)
    elif social_media == "facebook":
        for site in site_array:  # populates follower_counts
            if pd.isna(site):
                follower_counts.append("")
            else:
                driver.get(site)
                follower_count = facebook_fc(driver)
                follower_counts.append(follower_count)
    elif social_media == "youtube":
        for site in site_array:  # populates follower_counts
            if pd.isna(site):
                follower_counts.append("")
            else:
                driver.get(site)
                follower_count = youtube_fc(driver)
                follower_counts.append(follower_count)
    driver.quit()
    return follower_counts
"""

# fc means follower count
def full_function(path_to_data_file, path_to_write_to):
    data_array = make_data_array(path_to_data_file)
    artist = data_array[:, 0]
    """
    # tiktok = data_array[:, 1]
    # instagram = data_array[:, 2]
    # twitter = data_array[:, 3]
    # facebook = data_array[:, 4]
    # youtube = data_array[:, 5]
    """

    col_to_name = {
        1: "tiktok",
        2: "instagram",
        3: "twitter",
        4: "facebook",
        5: "youtube",
    }

    filled_data = artist
    for col in range(1, 6):
        site_array = data_array[:, col]
        follower_counts = fill_one_fc(col_to_name[col], site_array)
        filled_data = np.column_stack((filled_data, follower_counts))

    print(filled_data)
    dataframe_filled = pd.DataFrame(filled_data)  # writes to csv
    write_to = Path(path_to_write_to)
    dataframe_filled.to_csv(write_to, index=False, header=titles)


full_function("eq subset large.csv", "eq subset large filled.csv")


driver.quit()
