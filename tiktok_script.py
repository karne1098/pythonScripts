import string
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path
import numpy as np


# site = "https://www.tiktok.com/@nickiminaj"
# driver.get(site)
# followers_web_elt = driver.find_element(  # gets the web element w subscriber count
#     by=By.XPATH,
#     value="/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[2]/strong",
# )
# follower_count = followers_web_elt.text
# print(follower_count)


def make_data_array(data_file):
    training = Path(data_file)
    titles = ["artist name", "youtube website", ""]
    dataframe = pd.read_csv(
        training,
        sep=",",
        delimiter=None,
        header="infer",
        names=titles,
        index_col=None,
        usecols=None,
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

    # NOTE assumption: no gaps (csv has youtube website for every artist), and there
    # is a header at the top (i.e. "youtube website")
    data = dataframe.to_numpy()
    # XXX print(len(youtube_sites))
    return data


# def full_function(path_to_data_file, path_to_write_to):
#     data_array = make_data_array(path_to_data_file)
#     site_array = data_array.copy()
#     site_array = site_array[1:, 1]  # returns array of sites
#     # print("data array")
#     # print(data_array)
#     # print("site array")
#     # print(site_array)
#     driver = webdriver.Chrome()  # makes browser
#     driver.implicitly_wait(0.5)

#     follower_counts = []
#     for site in site_array:  # populates follower_counts
#         driver.get(site)
#         followers_web_elt = (
#             driver.find_element(  # gets the web element w subscriber count
#                 by=By.XPATH,
#                 value="/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[2]/strong",
#             )
#         )
#         follower_count = followers_web_elt.text  # parses subscriber count
#         follower_counts.append(follower_count)

#     driver.quit()

#     follower_counts.insert(  # adds title back and stacks w prev data
#         0, "follower counts"
#     )
#     # print(follower_counts)
#     a = data_array[:, :2]
#     # print("a")
#     # print(a)
#     data_filled_subs = np.column_stack((a, follower_counts))
#     # print(data_filled_subs)

#     dataframe_filled_subs = pd.DataFrame(data_filled_subs)  # writes to csv
#     write_to = Path(path_to_write_to)
#     dataframe_filled_subs.to_csv(write_to, index=False, header=False)


# function to keep 200 as 200 and change 1.7k --> 1,700 and 16.2m --> 16,200,000
def parse_count(text_number):
    tens = {"K": 1000, "M": 1000000}
    text_number = text_number.upper()
    if (text_number[-1] == "K") or (text_number[-1] == "M"):
        return int(float(text_number[:-1]) * tens[text_number[-1]])
    else:
        return int(text_number)


# testing parse_count
"""
ls = []
ls.append(parse_count("2"))
ls.append(parse_count("20"))
ls.append(parse_count("200"))
ls.append(parse_count("2K"))
ls.append(parse_count("2.3k"))
ls.append(parse_count("12.3K"))
ls.append(parse_count("122.3k"))
ls.append(parse_count("10K"))
ls.append(parse_count("2M"))
ls.append(parse_count("2.7M"))
ls.append(parse_count("200M"))
print(ls)
"""


def full_function(path_to_data_file, path_to_write_to):
    data_array = make_data_array(path_to_data_file)
    site_array = data_array.copy()
    site_array = site_array[1:, 1]  # returns array of sites
    driver = webdriver.Chrome()  # makes browser
    driver.implicitly_wait(0.5)

    follower_counts = []
    for site in site_array:  # populates follower_counts
        if pd.isna(site):
            follower_counts.append("")
        else:
            driver.get(site)
            followers_web_elt = driver.find_element(  # gets the web element w subscriber count
                by=By.XPATH,
                value="/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[2]/strong",
            )
            follower_count = parse_count(
                followers_web_elt.text
            )  # parses subscriber count
            follower_counts.append(follower_count)
    driver.quit()

    follower_counts.insert(  # adds title back and stacks w prev data
        0, "follower counts"
    )
    # print(follower_counts)
    a = data_array[:, :2]
    # print("a")
    # print(a)
    data_filled_subs = np.column_stack((a, follower_counts))
    # print(data_filled_subs)

    dataframe_filled_subs = pd.DataFrame(data_filled_subs)  # writes to csv
    write_to = Path(path_to_write_to)
    dataframe_filled_subs.to_csv(write_to, index=False, header=False)


# full_function("tiktok1.csv", "tiktok2.csv")

full_function("tiktok_spaces.csv", "tiktok_spaces_filled.csv")
