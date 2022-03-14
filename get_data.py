import requests
import ncaa_utils as utils
from tqdm import tqdm
import time
import numpy as np
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import random

DATA_DIR = "data"


def format_data(soup):
    tags = soup.find_all("tr")
    splittags = str(tags).split(",")

    splittable = [re.sub(r"<.*?>", ",", i) for i in splittags]
    splittable = [
        x.replace(",\n,", "")
        .replace(",,,", ",")
        .replace(",,", ",")
        .replace("]", "")
        .strip()
        for x in splittable
    ]
    splittable = [i for i in splittable if i[0].isdigit()]
    df = pd.DataFrame([i.split(",") for i in splittable])
    df[2] = np.where(df[2] == " ", df[2], None)
    try:
        df = df.dropna().reset_index(drop=True).drop(columns={0, 2, 23})
    except Exception as e:
        print(e)
    df["Rk"] = np.arange(1, df.shape[0] + 1)
    columns = [
        "Team",
        "Seed",
        "Conf",
        "W-L",
        "AdjEM",
        "AdjO",
        "AdjO_rank",
        "AdjD",
        "AdjD_rank",
        "AdjT",
        "AdjT_rank",
        "Luck",
        "Luck_rank",
        "AdjEM",
        "AdjEM_rank",
        "OppO",
        "OppO_rank",
        "OppD",
        "OppD_rank",
        "NCSOS_AdjEM",
        "NCSOS_AdjEM_rank",
        "Rk",
    ]
    df.columns = columns
    return df


if __name__ == "__main__":
    kenpom_url = "https://kenpom.com"
    page = requests.get(kenpom_url)
    soup = bs(page.text, "html.parser")
    links = [x.get("href") for x in soup.find_all("a")]
    yearlinks = [x for x in links if str(x)[0:13] == "/index.php?y="]
    years = [x.replace("/index.php?y=", "") for x in yearlinks]
    maindf = pd.DataFrame()
    for link in tqdm(yearlinks):
        page = requests.get(kenpom_url + link)
        soup = bs(page.text, "html.parser")
        df = format_data(soup)
        maindf = maindf.append(df)
        time.sleep(random.randint(3, 15))
    maindf.to_csv(f"{DATA_DIR}/kenpom_data.csv", index=False)

    kenpom_url = "https://kenpom.com"
    page = requests.get(kenpom_url)
    soup = bs(page.text, "html.parser")
    # THIS YEARS 64 teams
    currentdf = format_data(soup)
    currentdf.to_csv(f"{DATA_DIR}/kenpom_current_data.csv", index=False)

    # CODE TO UPDATE CONFIG
    # untested
    firstfour, west, east, south, midwest = utils.get_bracket()
    import yaml
    with open("ncaa_config.yml") as f:
        config = yaml.load(f)
    # to do: replace all St or State with St.
    # fix brackets in config in which teams are in

    config["TEAMS"]["EAST"] = east
    config["TEAMS"]["WEST"] = west
    config["TEAMS"]["MIDWEST"] = midwest
    config["TEAMS"]["SOUTH"] = south
    with open("ncaa_config.yml", "w+") as f:
        yaml.dump(f)
