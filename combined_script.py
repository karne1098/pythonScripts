from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from time import sleep

driver = webdriver.Chrome()  # makes browser
driver.implicitly_wait(0.5)

titles = [  # these must be the column names in your excel csv
    "artist name",
    "tiktok",
    "instagram",
    "twitter",
    "facebook",
    "youtube",
    "personal",
    "spotify",
]


def make_data_array(data_file):
    """
    makes usable data array from csv w/ links

    data_file: the csv file containing the links for each social,
        ex. "bts_members.csv", make sure the file is in the same folder as
        combined_script.py
    """

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


def parse_count(text_number):
    """
    keeps 200-->200, makes 1.7k --> 1700 and 16.2M --> 16200000
    """
    tens = {"K": 1000, "M": 1000000}
    text_number = text_number.upper()
    if (text_number[-1] == "K") or (text_number[-1] == "M"):
        return int(float(text_number[:-1]) * tens[text_number[-1]])
    else:
        if "," in text_number:
            text_number = text_number.replace(",", "")
        return int(text_number)


def instagram_fc():
    """
    assuming our driver has retrieved the instagram profile, this returns the
    number of followers the profile has OR "mannual" if there are any issues
    retrieving the follower count
    """

    try:
        # makes the script more human-like, trying to find web-elt every 2 secs
        followers_web_elt = WebDriverWait(driver, 5, 2).until(
            EC.presence_of_element_located(
                (
                    # XPATH is like direct path to element
                    By.XPATH,
                    "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul",
                )
            )
        )
        # get text of web-elt
        unparsed_str = followers_web_elt.text
        # isolates "___ followers" from the text superset
        unparsed_fc = re.findall("[\w|,]+ followers", unparsed_str)[0]
        # parses "___ followers" to pure number
        fc = parse_count(unparsed_fc.split(" ")[0])
    except:
        fc = "mannual"
    return fc


def tiktok_fc():
    """
    assuming our driver has retrieved the tiktok profile, this returns the
    number of followers the profile has OR "mannual" if there are any issues
    retrieving the follower count
    """
    try:
        followers_web_elt = driver.find_element(
            by=By.XPATH,
            value="/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[2]/strong",
        )
        fc = parse_count(followers_web_elt.text)
    except:
        fc = "mannual"
    return fc


def twitter_fc():
    """
    assuming our driver has retrieved the twitter profile, this returns the
    number of followers the profile has OR "mannual" if there are any issues
    retrieving the follower count
    """
    try:
        followers_web_elt = driver.find_element(
            by=By.XPATH,
            value="/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[5]/div[2]/a/span[1]/span",
        )
        fc = parse_count(followers_web_elt.text)
    except:
        try:
            followers_web_elt = driver.find_element(
                # this means "Followers" is contained within the text of the
                # web-elt. the web-elt must be of the 'link' type
                by=By.PARTIAL_LINK_TEXT,
                value="Followers",
            )
            fc_unparsed = followers_web_elt.text.split(" ")[0]
            fc = parse_count(fc_unparsed)
        except:
            try:
                followers_web_elt = driver.find_element(
                    by=By.XPATH,
                    value="/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[4]/div[2]/a/span[1]/span",
                )
                fc = parse_count(followers_web_elt.text)
            except:
                try:
                    followers_web_elt = driver.find_element(
                        by=By.XPATH,
                        value="/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[1]/div/div[5]/div[2]/div/span[1]/span",
                    )  #
                    fc = parse_count(followers_web_elt.text)
                except:
                    fc = "manual"
    return fc


def facebook_fc():
    """
    assuming our driver has retrieved the facebook profile, this returns the
    number of followers or likes the profile has OR "mannual" if there's issues
    retrieving the follower count
    """
    try:
        followers_web_elt = driver.find_element(
            by=By.PARTIAL_LINK_TEXT, value="followers"
        )
        fc = parse_count(followers_web_elt.text.split(" ")[0])

    except:
        try:
            followers_web_elt = driver.find_element(
                by=By.PARTIAL_LINK_TEXT, value="likes"
            )
            fc = parse_count(followers_web_elt.text.split(" ")[0])

        except:
            try:
                followers_web_elt = driver.find_element(
                    by=By.XPATH,
                    value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[1]",
                )
                fc = parse_count(followers_web_elt.text.split(" ")[0])

            except:

                try:
                    followers_web_elt = driver.find_element(
                        by=By.XPATH,
                        value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div",
                    )
                    unparsed_str = followers_web_elt.text
                    unparsed_fc = re.findall(
                        "[\w|,]+ people follow this", unparsed_str
                    )[0]
                    fc = parse_count(unparsed_fc.split(" ")[0])

                except:
                    fc = "manual"
    return fc


def youtube_fc():
    """
    assuming our driver has retrieved the youtube profile, this returns the
    number of followers the profile has OR "mannual" if there are any issues
    retrieving the follower count
    """
    try:
        followers_web_elt = driver.find_element(  # gets the web element w subscriber count
            by=By.XPATH,
            value="/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/yt-formatted-string",
        )
        fc_unparsed = followers_web_elt.text.split(" ")[0]  # parses subscriber count
        fc = parse_count(fc_unparsed)
    except:
        fc = "manual"
    return fc


def spotify_fc():
    """
    assuming our driver has retrieved the spotify profile, this returns the
    number of followers the profile has OR "mannual" if there are any issues
    retrieving the follower count
    """
    try:
        followers_web_elt = WebDriverWait(driver, 5, 2).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[3]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[1]",
                )
            )
        )
        unparsed_str = followers_web_elt.text
        unparsed_fc = re.findall("[\w|,]+ monthly listeners", unparsed_str)[0]
        fc = unparsed_fc.split(" ")[0]
        sleep(1)
    except:
        try:
            followers_web_elt = WebDriverWait(driver, 5, 2).until(
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
            sleep(1)
        except:
            fc = "mannual"
    return fc


def fill_one_fc(social_media, site_array):
    """
    takes in the type of social media, and a site array that represents one
    column of data (list of links to instagrams)
    """
    follower_counts = []  # array to be populated with follower counts
    if social_media == "personal":  # for the column with personal link,
        follower_counts = [""] * len(site_array)  # populate with nothing
    else:
        for site in site_array:
            if pd.isna(site):  # if a particular person doesn't have this social
                follower_counts.append("")
            else:
                try:
                    driver.get(site)
                    follower_count = eval(social_media + "_fc()")
                    follower_counts.append(follower_count)
                except:
                    follower_counts.append("mannual")
    return follower_counts


# fc means follower count
def full_function(path_to_data_file, path_to_write_to):
    """
    executes the process of taking in the data from path_to_data_file, finds
    out all of the follower counts, and outputs info to path_to_write_to
    """
    data_array = make_data_array(path_to_data_file)
    artist = data_array[:, 0]  # gets artist column

    col_to_name = {
        1: "tiktok",
        2: "instagram",
        3: "twitter",
        4: "facebook",
        5: "youtube",
        6: "personal",
        7: "spotify",
    }

    filled_data = artist  # initialize the filled array with the artists
    for col in range(1, 8):  # picking the range of social medias to do
        site_array = data_array[:, col]
        follower_counts = fill_one_fc(col_to_name[col], site_array)
        # updating filled array
        filled_data = np.column_stack((filled_data, follower_counts))

    # turns filled array into dataframe and writes to csv
    dataframe_filled = pd.DataFrame(filled_data)
    write_to = Path(path_to_write_to)
    dataframe_filled.to_csv(write_to, index=False, header=titles)


# change the first and second arguments as applicable
full_function("eq subset 2.csv", "eq subset filled.csv")

# quits the driver so it doesn't continue endlessly
driver.quit()
