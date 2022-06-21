from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path
import numpy as np

# NOTE: here is where we work on using csv's

# takes a path string and outputs an array with data
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
        skip_blank_lines=True,
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


def full_function(path_to_data_file, path_to_write_to):
    data_array = make_data_array(path_to_data_file)
    site_array = data_array.copy()
    site_array = site_array[1:, 1]  # returns array of sites
    # print("data array")
    # print(data_array)
    # print("site array")
    # print(site_array)
    driver = webdriver.Chrome()  # makes browser
    driver.implicitly_wait(0.5)

    follower_counts = []
    for site in site_array:  # populates follower_counts
        driver.get(site)
        followers_web_elt = driver.find_element(  # gets the web element w subscriber count
            by=By.XPATH,
            value="/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/yt-formatted-string",
        )
        follower_count = followers_web_elt.text.split(" ")[0]  # parses subscriber count
        follower_counts.append(follower_count)

    driver.quit()

    follower_counts.insert(
        0, "follower counts"
    )  # adds title back and stacks w prev data
    # print(follower_counts)
    a = data_array[:, :2]
    # print("a")
    # print(a)
    data_filled_subs = np.column_stack((a, follower_counts))
    # print(data_filled_subs)

    dataframe_filled_subs = pd.DataFrame(data_filled_subs)
    write_to = Path(path_to_write_to)
    dataframe_filled_subs.to_csv(write_to, index=False, header=False)


full_function("you1.csv", "you2.csv")
