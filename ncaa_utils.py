from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup as bs
import seaborn as sns
import pandas as pd

firstround = {
    1: [[1, 16], [8, 9], [5, 12], [4, 13], [6, 11], [3, 14], [7, 10], [2, 15]],
    2: [[1, 16], [8, 9], [5, 12], [4, 13], [6, 11], [3, 14], [7, 10], [2, 15]],
    3: [[1, 16], [8, 9], [5, 12], [4, 13], [6, 11], [3, 14], [7, 10], [2, 15]],
    4: [[1, 16], [8, 9], [5, 12], [4, 13], [6, 11], [3, 14], [7, 10], [2, 15]],
}


def construct1stround(df):
    region = [1, 2, 3, 4]
    for i in region:
        for j in range(len(firstround[i])):
            seeds = firstround[i][j]
            print("seeds", seeds)
            if i == 1:
                print(df[(df.Region == 0) & (df.Seed == seeds[0])])
                team1 = df[(df.Region == 0) & (df.Seed == seeds[0])].index[0]
                team2 = df[(df.Region == 0) & (df.Seed == seeds[1])].index[0]
            if i == 4:
                team1 = df[(df.Region == 3) & (df.Seed == seeds[0])].index[0]
                team2 = df[(df.Region == 3) & (df.Seed == seeds[1])].index[0]
            if i == 3:
                team1 = df[(df.Region == 2) & (df.Seed == seeds[0])].index[0]
                team2 = df[(df.Region == 2) & (df.Seed == seeds[1])].index[0]
            if i == 2:
                team1 = df[(df.Region == 1) & (df.Seed == seeds[0])].index[0]
                team2 = df[(df.Region == 1) & (df.Seed == seeds[1])].index[0]
            firstround[i][j] = [team1, team2]
    return firstround


def construct2ndround(winners):
    _round = {
        1: [winners[0], winners[1]],
        2: [winners[2], winners[3]],
        3: [winners[4], winners[5]],
        4: [winners[6], winners[7]],
    }
    return _round


def construct3rdround(winners):
    print(winners)
    _round = {
        1: [winners[0], winners[1]],
        2: [winners[2], winners[3]],
    }
    return _round


def construct4thround(winners):
    _round = {
        1: [winners[0], winners[1]],
    }
    return _round


def construct5thround(winner1, winner2):
    _round = {
        1: [winner1[0], winner2[0]],
    }
    return _round


def constructfinalround(winner1, winner2):
    _round = {
        1: (winner1, winner2),
    }
    return _round


def assign_playoff_city(df):
    df["firstrds"] = np.nan
    df.loc[
        (df.Region == 0) & ((df.Seed == 1) | (df.Seed == 16)), "firstrds"
    ] = "Columbia"
    df.loc[
        (df.Region == 0) & ((df.Seed == 8) | (df.Seed == 9)), "firstrds"
    ] = "Columbia"
    df.loc[
        (df.Region == 0) & ((df.Seed == 5) | (df.Seed == 12)), "firstrds"
    ] = "San Jose"
    df.loc[
        (df.Region == 0) & ((df.Seed == 4) | (df.Seed == 13)), "firstrds"
    ] = "San Jose"
    df.loc[
        (df.Region == 0) & ((df.Seed == 6) | (df.Seed == 11)), "firstrds"
    ] = "Jacksonville"
    df.loc[
        (df.Region == 0) & ((df.Seed == 3) | (df.Seed == 14)), "firstrds"
    ] = "Jacksonville"
    df.loc[
        (df.Region == 0) & ((df.Seed == 7) | (df.Seed == 10)), "firstrds"
    ] = "Des Moines"
    df.loc[
        (df.Region == 0) & ((df.Seed == 2) | (df.Seed == 15)), "firstrds"
    ] = "Des Moines"

    df.loc[
        (df.Region == 1) & ((df.Seed == 1) | (df.Seed == 16)), "firstrds"
    ] = "Columbus"
    df.loc[
        (df.Region == 1) & ((df.Seed == 8) | (df.Seed == 9)), "firstrds"
    ] = "Columbus"
    df.loc[
        (df.Region == 1) & ((df.Seed == 5) | (df.Seed == 12)), "firstrds"
    ] = "Salt Lake City"
    df.loc[
        (df.Region == 1) & ((df.Seed == 4) | (df.Seed == 13)), "firstrds"
    ] = "Salt Lake City"
    df.loc[(df.Region == 1) & ((df.Seed == 6) | (
        df.Seed == 11)), "firstrds"] = "Tulsa"
    df.loc[(df.Region == 1) & ((df.Seed == 3) | (
        df.Seed == 14)), "firstrds"] = "Tulsa"
    df.loc[
        (df.Region == 1) & ((df.Seed == 7) | (df.Seed == 10)), "firstrds"
    ] = "Jacksonville"
    df.loc[
        (df.Region == 1) & ((df.Seed == 2) | (df.Seed == 15)), "firstrds"
    ] = "Jacksonville"

    df.loc[
        (df.Region == 2) & ((df.Seed == 1) | (df.Seed == 16)), "firstrds"
    ] = "Columbia"
    df.loc[
        (df.Region == 2) & ((df.Seed == 8) | (df.Seed == 9)), "firstrds"
    ] = "Columbia"
    df.loc[
        (df.Region == 2) & ((df.Seed == 5) | (df.Seed == 12)), "firstrds"
    ] = "San Jose"
    df.loc[
        (df.Region == 2) & ((df.Seed == 4) | (df.Seed == 13)), "firstrds"
    ] = "San Jose"
    df.loc[
        (df.Region == 2) & ((df.Seed == 6) | (df.Seed == 11)), "firstrds"
    ] = "Hartford"
    df.loc[
        (df.Region == 2) & ((df.Seed == 3) | (df.Seed == 14)), "firstrds"
    ] = "Hartford"
    df.loc[
        (df.Region == 2) & ((df.Seed == 7) | (df.Seed == 10)), "firstrds"
    ] = "Columbus"
    df.loc[
        (df.Region == 2) & ((df.Seed == 2) | (df.Seed == 15)), "firstrds"
    ] = "Columbus"

    df.loc[
        (df.Region == 3) & ((df.Seed == 1) | (df.Seed == 16)), "firstrds"
    ] = "Salt Lake City"
    df.loc[
        (df.Region == 3) & ((df.Seed == 8) | (df.Seed == 9)), "firstrds"
    ] = "Salt Lake City"
    df.loc[
        (df.Region == 3) & ((df.Seed == 5) | (df.Seed == 12)), "firstrds"
    ] = "Hartford"
    df.loc[
        (df.Region == 3) & ((df.Seed == 4) | (df.Seed == 13)), "firstrds"
    ] = "Hartford"
    df.loc[(df.Region == 3) & ((df.Seed == 6) | (
        df.Seed == 11)), "firstrds"] = "Tulsa"
    df.loc[(df.Region == 3) & ((df.Seed == 3) | (
        df.Seed == 14)), "firstrds"] = "Tulsa"
    df.loc[
        (df.Region == 3) & ((df.Seed == 7) | (df.Seed == 10)), "firstrds"
    ] = "Des Moines"
    df.loc[
        (df.Region == 3) & ((df.Seed == 2) | (df.Seed == 15)), "firstrds"
    ] = "Des Moines"

    df["midrds"] = np.nan
    df.loc[
        (df.Region == 0) & ((df.Seed == 1) | (df.Seed == 16)), "midrds"
    ] = "Washington D.C."
    df.loc[
        (df.Region == 0) & ((df.Seed == 8) | (df.Seed == 9)), "midrds"
    ] = "Washington D.C."
    df.loc[
        (df.Region == 0) & ((df.Seed == 5) | (df.Seed == 12)), "midrds"
    ] = "Washington D.C."
    df.loc[
        (df.Region == 0) & ((df.Seed == 4) | (df.Seed == 13)), "midrds"
    ] = "Washington D.C."
    df.loc[
        (df.Region == 0) & ((df.Seed == 6) | (df.Seed == 11)), "midrds"
    ] = "Washington D.C."
    df.loc[
        (df.Region == 0) & ((df.Seed == 3) | (df.Seed == 14)), "midrds"
    ] = "Washington D.C."
    df.loc[
        (df.Region == 0) & ((df.Seed == 7) | (df.Seed == 10)), "midrds"
    ] = "Washington D.C."
    df.loc[
        (df.Region == 0) & ((df.Seed == 2) | (df.Seed == 15)), "midrds"
    ] = "Washington D.C."

    df.loc[
        (df.Region == 1) & ((df.Seed == 1) | (df.Seed == 16)), "midrds"
    ] = "Kansas City"
    df.loc[
        (df.Region == 1) & ((df.Seed == 8) | (df.Seed == 9)), "midrds"
    ] = "Kansas City"
    df.loc[
        (df.Region == 1) & ((df.Seed == 5) | (df.Seed == 12)), "midrds"
    ] = "Kansas City"
    df.loc[
        (df.Region == 1) & ((df.Seed == 4) | (df.Seed == 13)), "midrds"
    ] = "Kansas City"
    df.loc[
        (df.Region == 1) & ((df.Seed == 6) | (df.Seed == 11)), "midrds"
    ] = "Kansas City"
    df.loc[
        (df.Region == 1) & ((df.Seed == 3) | (df.Seed == 14)), "midrds"
    ] = "Kansas City"
    df.loc[
        (df.Region == 1) & ((df.Seed == 7) | (df.Seed == 10)), "midrds"
    ] = "Kansas City"
    df.loc[
        (df.Region == 1) & ((df.Seed == 2) | (df.Seed == 15)), "midrds"
    ] = "Kansas City"

    df.loc[
        (df.Region == 2) & ((df.Seed == 1) | (df.Seed == 16)), "midrds"
    ] = "Louisville"
    df.loc[
        (df.Region == 2) & ((df.Seed == 8) | (df.Seed == 9)), "midrds"
    ] = "Louisville"
    df.loc[
        (df.Region == 2) & ((df.Seed == 5) | (df.Seed == 12)), "midrds"
    ] = "Louisville"
    df.loc[
        (df.Region == 2) & ((df.Seed == 4) | (df.Seed == 13)), "midrds"
    ] = "Louisville"
    df.loc[
        (df.Region == 2) & ((df.Seed == 6) | (df.Seed == 11)), "midrds"
    ] = "Louisville"
    df.loc[
        (df.Region == 2) & ((df.Seed == 3) | (df.Seed == 14)), "midrds"
    ] = "Louisville"
    df.loc[
        (df.Region == 2) & ((df.Seed == 7) | (df.Seed == 10)), "midrds"
    ] = "Louisville"
    df.loc[
        (df.Region == 2) & ((df.Seed == 2) | (df.Seed == 15)), "midrds"
    ] = "Louisville"

    df.loc[(df.Region == 3) & ((df.Seed == 1) | (
        df.Seed == 16)), "midrds"] = "Anaheim"
    df.loc[(df.Region == 3) & ((df.Seed == 8) |
                               (df.Seed == 9)), "midrds"] = "Anaheim"
    df.loc[(df.Region == 3) & ((df.Seed == 5) | (
        df.Seed == 12)), "midrds"] = "Anaheim"
    df.loc[(df.Region == 3) & ((df.Seed == 4) | (
        df.Seed == 13)), "midrds"] = "Anaheim"
    df.loc[(df.Region == 3) & ((df.Seed == 6) | (
        df.Seed == 11)), "midrds"] = "Anaheim"
    df.loc[(df.Region == 3) & ((df.Seed == 3) | (
        df.Seed == 14)), "midrds"] = "Anaheim"
    df.loc[(df.Region == 3) & ((df.Seed == 7) | (
        df.Seed == 10)), "midrds"] = "Anaheim"
    df.loc[(df.Region == 3) & ((df.Seed == 2) | (
        df.Seed == 15)), "midrds"] = "Anaheim"
    return df


def plot_df(df):
    plt.figure(1)
    g = sns.scatterplot(data=df, x="AdjEM", y="Luck", color="m")
    for line in range(0, df.shape[0]):
        g.text(
            df.AdjEM[line] + 0.01,
            df.Luck[line],
            df.index[line],
            horizontalalignment="left",
            size="medium",
            color="black",
            weight="semibold",
        )
    plt.figure(2)
    g = sns.scatterplot(x="AdjO", y="AdjD", data=df, color="m")
    for line in range(0, df.shape[0]):
        g.text(
            df.AdjO[line] + 0.01,
            df.AdjD[line],
            df.index[line],
            horizontalalignment="left",
            size="medium",
            color="black",
            weight="semibold",
        )
    plt.figure(3)
    g = sns.scatterplot(data=df, x="AdjT", y="AdjO", color="g")
    for line in range(0, df.shape[0]):
        g.text(
            df.AdjT[line] + 0.01,
            df.AdjO[line],
            df.index[line],
            horizontalalignment="left",
            size="medium",
            color="black",
            weight="semibold",
        )
    plt.figure(4)
    g = sns.scatterplot(data=df, x="AdjEM.1", y="AdjD", color="g")
    for line in range(0, df.shape[0]):
        g.text(
            df["AdjEM.1"][line] + 0.01,
            df.AdjD[line],
            df.index[line],
            horizontalalignment="left",
            size="medium",
            color="black",
            weight="semibold",
        )


def get_bracket():
    bracket_link = "http://www.espn.com/mens-college-basketball/tournament/bracket"
    espn = requests.get(bracket_link)
    soup = bs(espn.text)
    teams = []
    for link in soup.findAll("a"):
        if link.get("title"):
            teams.append(link.get("title"))

    return bracket_form(teams)


def bracket_form(teams):
    first_four = teams[:8]
    west = teams[8:22]
    east = teams[22:36]
    south = teams[36:52]
    midwest = teams[52:68]
    return first_four, west, east, south, midwest
