import pandas as pd
import seaborn as sns
from collections import Counter
from sklearn import preprocessing

# from geopy.geocoders import Nominatim
import matplotlib
from matplotlib import pyplot as plt
import ncaa_utils as utils
import numpy as np
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from tqdm import tqdm
import yaml
import logging
import argparse
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier as rf

logger = logging.getLogger()
logger.setLevel(logging.INFO)

with open("ncaa_config_new.yml", "r") as f:
    config = yaml.load(f)
DATA_DIR = config["DATA_DIR"]
midwest = config["TEAMS"]["MIDWEST"]
west = config["TEAMS"]["WEST"]
south = config["TEAMS"]["SOUTH"]
EAST_CITIES = config["CITIES"]["EAST"]
SOUTH_CITIES = config["CITIES"]["SOUTH"]
WEST_CITIES = config["CITIES"]["WEST"]
MIDWEST_CITIES = config["CITIES"]["MIDWEST"]
firstround = {
    1: [[1, 16], [8, 9], [5, 12], [4, 13], [6, 11], [3, 14], [7, 10], [2, 15]],
    2: [[1, 16], [8, 9], [5, 12], [4, 13], [6, 11], [3, 14], [7, 10], [2, 15]],
    3: [[1, 16], [8, 9], [5, 12], [4, 13], [6, 11], [3, 14], [7, 10], [2, 15]],
    4: [[1, 16], [8, 9], [5, 12], [4, 13], [6, 11], [3, 14], [7, 10], [2, 15]],
}
NUM_SIMS = config["MODEL_CONFIG"]["NUM_SIMS"]
RISK_FACTOR = config["MODEL_CONFIG"]["RANDOM_FACTOR"]


def matchupwinner(region_, roundnum, bracket=firstround):
    winners = []
    single = 0
    region_num = 0
    noregion = False
    # get region
    if region_ == "East":
        region_num = 1
    elif region_ == "Midwest":
        region_num = 2
    elif region_ == "South":
        region_num = 3
    elif region_ == "West":
        region_num = 4
    elif region_ == "noregion":
        noregion = True
    if roundnum == 1:
        numteams = range(1, 9)
    if roundnum == 2:
        numteams = range(1, 5)
    if roundnum == 3:
        numteams = range(1, 3)
    if roundnum == 4:
        numteams = range(1, 2)
    if roundnum == 5:
        numteams = range(1, 2)
    if roundnum == 1:
        for matchup in range(len(bracket[region_num])):
            matchup1 = bracket[region_num][matchup][0]
            matchup2 = bracket[region_num][matchup][1]
            teams = []
            teams.append(matchup1)
            teams.append(matchup2)
            """
            newdf = df.drop(teams)
            x = newdf.drop(columns = 'Rk')
            y = newdf.Rk
            gnb.fit(x,y)
            """
            d = df[df.index == teams[0]].drop(columns=["Rk", "Region"])
            n = df[df.index == teams[1]].drop(columns=["Rk", "Region"])
            if clf.predict(d) < clf.predict(n):
                # logging.info(teams[0])
                winners.append(teams[0])
            else:
                # logging.info(teams[1])
                winners.append(teams[1])
    # logging.info(gnb.predict(d),gnb.predict(n))
    else:
        for matchup in numteams:
            matchup1 = bracket[matchup][0]
            matchup2 = bracket[matchup][1]
            teams = []
            teams.append(matchup1)
            teams.append(matchup2)
            print(teams)
            newdf = df.drop(teams)
            """
            x = newdf.drop(columns = 'Rk')
            y = newdf.Rk
            gnb.fit(x,y)
            """
            d = df[df.index == teams[0]].drop(columns=["Rk", "Region"])
            n = df[df.index == teams[1]].drop(columns=["Rk", "Region"])
            if clf.predict(d) < clf.predict(n):
                logging.info(teams[0])
                winners.append(teams[0])
            else:
                logging.info(teams[1])
                winners.append(teams[1])
    # logging.info(gnb.predict(d),gnb.predict(n))
    return winners


def preprocess(df, current=False):
    """
    dfkeep = []
    for row in df.itertuples():
        team = row.Team
        if str.isnumeric(team[len(team)-1]):
            dfkeep.append(row[0])
    df = df.loc[dfkeep]
    school = []
    seed = []
    for row in df.itertuples():
        index = row.Index
        team = row.Team
        if str.isnumeric(team[-2:]):
            school.append(team[:-2])
            seed.append(team[-2:])
        else:
            school.append(team[:-1])
            seed.append(team[-1:])
    df['Team_'] =school
    df.Team_ = df.Team_.str.rstrip()
    df['Seed'] =  seed
    df.Seed = pd.to_numeric(df.Seed)
    """

    if "Unnamed: 0" in df.columns:
        df.drop(columns=["Unnamed: 0"], inplace=True)
    a = df["W-L"].str.split("-")
    df["Win"] = [x[0] for x in a]
    df["Loss"] = [x[1] for x in a]
    if current:
        df["Region"] = "East"
        df.loc[df["Team"].isin(west), ["Region"]] = "West"
        df.loc[df["Team"].isin(midwest), ["Region"]] = "Midwest"
        df.loc[df["Team"].isin(south), ["Region"]] = "South"
        le = preprocessing.LabelEncoder()
        le.fit(df.Region)
        df.Region = le.transform(df.Region)
    df.drop(columns=["Conf", "W-L"], inplace=True)
    df.set_index("Team", inplace=True)
    df["Random_Bias"] = (
        np.random.randint(low=50, high=500, size=df.shape[0])
        + (df.Rk) * RISK_FACTOR * 1
    )
    df = shuffle(df)

    return df


def train_data(df):

    gnb = GaussianNB()
    x = df.drop(columns="Rk")
    y = df.Rk
    gnb.fit(x, y)
    rf_clf = rf(n_estimators=100, max_depth=10, random_state=0)
    rf_clf.fit(x, y)
    return rf_clf, gnb


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate a March Madness Bracket with GNB trained by KenPom Data"
    )
    parser.add_argument("--data", dest="data_path", help="data path")
    parser.add_argument("--plot", dest="plot", help="true or false")
    args = parser.parse_args()
    data_folder = args.data_path
    plots = False
    plots = args.plot
    datadf = pd.read_csv(f"{data_folder}")
    datadf = preprocess(datadf)
    df = pd.read_csv(f"data/kenpom_current_data_final.csv")
    # df = pd.read_csv(f"data/kenpom_data.csv")

    df.Team = [x.replace("amp;M;", "M") for x in list(df.Team)]
    newdf = pd.DataFrame()
    for i in range(1, 17):
        newdf = newdf.append(df[df.Seed == i][:4])
    df = preprocess(newdf, True)
    # initialize model
    rf_clf, gnb = train_data(datadf)
    clf = rf_clf
    # gnb = GaussianNB()
    # logging.info(regionalpha, region_word)
    logging.info(df)
    num_champs = []
    num_finalfour = []
    # init round construction
    firstround = utils.construct1stround(df)
    for i in tqdm(range(1, NUM_SIMS)):
        inc = i
        df["Random_Bias"] = np.random.randint(
            low=100, high=1000, size=df.shape[0])
        +(df.Rk) * RISK_FACTOR * inc
        east2 = utils.construct2ndround(
            matchupwinner("East", roundnum=1, bracket=firstround)
        )
        west2 = utils.construct2ndround(
            matchupwinner("West", roundnum=1, bracket=firstround)
        )
        midwest2 = utils.construct2ndround(
            matchupwinner("Midwest", roundnum=1, bracket=firstround)
        )
        south2 = utils.construct2ndround(
            matchupwinner("South", roundnum=1, bracket=firstround)
        )
        logging.info("---ROUND 2 - Round of 32---")
        logging.info(east2)
        logging.info(west2)
        logging.info(south2)
        logging.info(midwest2)

        east3 = utils.construct3rdround(
            matchupwinner("East", roundnum=2, bracket=east2)
        )
        west3 = utils.construct3rdround(
            matchupwinner("West", roundnum=2, bracket=west2)
        )
        midwest3 = utils.construct3rdround(
            matchupwinner("Midwest", roundnum=2, bracket=midwest2)
        )
        south3 = utils.construct3rdround(
            matchupwinner("South", roundnum=2, bracket=south2)
        )
        logging.info("---ROUND 3 - SWEET 16---")
        logging.info(east3)
        logging.info(west3)
        logging.info(south3)
        logging.info(midwest3)
        east4 = utils.construct4thround(
            matchupwinner("East", roundnum=3, bracket=east3)
        )
        west4 = utils.construct4thround(
            matchupwinner("West", roundnum=3, bracket=west3)
        )
        midwest4 = utils.construct4thround(
            matchupwinner("Midwest", roundnum=3, bracket=midwest3)
        )
        south4 = utils.construct4thround(
            matchupwinner("South", roundnum=3, bracket=south3)
        )
        logging.info("--- ELITE 8 ---")
        logging.info(east4)
        logging.info(west4)
        logging.info(south4)
        logging.info(midwest4)
        eastwest = utils.construct5thround(
            matchupwinner("noregion", roundnum=4, bracket=east4),
            matchupwinner("West", roundnum=4, bracket=west4),
        )
        southmidwest = utils.construct5thround(
            matchupwinner("noregion", roundnum=4, bracket=midwest4),
            matchupwinner("South", roundnum=4, bracket=south4),
        )
        num_finalfour = num_finalfour + eastwest[1] + southmidwest[1]
        logging.info("--- FINAL 4 ---")
        logging.info(eastwest)
        logging.info(southmidwest)
        final = utils.construct5thround(
            matchupwinner("noregion", roundnum=4, bracket=eastwest),
            matchupwinner("West", roundnum=4, bracket=southmidwest),
        )
        logging.info("--- FINAL ---")
        logging.info(final)
        champ = matchupwinner("noregion", roundnum=4, bracket=final)
        logging.info("---- CHAMPION ----")
        logging.info(champ)
        num_champs.append(champ[0])
    final4_count = Counter(num_finalfour)

    count = Counter(num_champs)
    df_count = (
        pd.DataFrame.from_dict(count, orient="index")
        .reset_index()
        .rename(columns={"index": "team", 0: "count"})
    )
    df_4count = (
        pd.DataFrame.from_dict(final4_count, orient="index")
        .reset_index()
        .rename(columns={"index": "team", 0: "count"})
    )
    if plots:
        # utils.plot_df(df)

        compare = df[(df.index == "UCLA")]
        print(compare)
        compare = df[(df.index == "UCLA") | (df.index == "Alabama")]
        print(compare)
        utils.plot_df(compare)
        plt.figure(0)
        sns.barplot(data=df_count, x="team", y="count").set(title="final")
        plt.figure(6)
        sns.barplot(data=df_4count, x="team", y="count").set(title="final4")
        plt.show()
