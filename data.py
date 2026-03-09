import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from math import *
from sys import argv

class Data:
    _data: pd.DataFrame
    _fname: str
    _siz: int

    def __init__(self, _fname="./data/summary26.csv", _siz=-1, _sort_axis_label="RankAdjEM"):
        """This class creates the data frame to draw the graphs."""
        self._fname = _fname
        self._data = pd.read_csv(_fname)
        self._data = self.read_four_factors()
        self._data = self._data.sort_values(_sort_axis_label, ascending=True)
        self._siz = _siz

    def __call__(self, _xaxis = "AdjOE", _yaxis = "AdjDE") -> None:
        """Calling the data frame as a callable object allows for creating a graph based on any axis in the main data set"""
        labels = self._data.index.tolist()
        ranks = self._data["RankAdjEM"]
        x_vals = self._data[_xaxis]
        y_vals = self._data[_yaxis]
    
        font = {'family' : 'serif',
                'weight' : 'bold',
                'size': 22}

        matplotlib.rc('font', **font)
        if(self._siz != -1):
            labels = labels[:self._siz]
            ranks = ranks[:self._siz]
            x_vals = x_vals[:self._siz]
            y_vals = y_vals[:self._siz]

        plt.xlabel(_xaxis)
        plt.ylabel(_yaxis)
        plt.title(f"{_xaxis} vs {_yaxis} (KenPom Top 50)")
        plt.scatter(x_vals, y_vals)
        ax = plt.gca()

        if _xaxis == "AdjDE":
            ax.invert_xaxis()
        elif _yaxis == "AdjDE":
            ax.invert_yaxis()

        for i, (x, y, label, rank) in enumerate(zip(x_vals, y_vals, labels, ranks)):
            print(f"{label} ({rank})")
            plt.text(x + 0.1, y + 0.2, f"{label} ({rank})", fontsize=8)

        plt.grid(True)
        plt.show()

    def read_four_factors(self):
        summary = pd.read_csv(self._fname)
        offense = pd.read_csv("./data/offense26.csv")
        defense = pd.read_csv("./data/defense26.csv")
        misc = pd.read_csv("./data/misc26.csv")
        combined_data = pd.merge(offense, self._data, on="TeamName")
        combined_data = pd.merge(combined_data, defense, on="TeamName")
        combined_data = pd.merge(combined_data, misc, on="TeamName")
        return combined_data.set_index("TeamName")

    def predict(self, teamNameA: str, teamNameB: str):
        """Complicated formula to estimate the outcome as a probability of each possession"""
        teamA = self._data.loc[teamNameA]
        teamB = self._data.loc[teamNameB]
        shooting_factor_A = teamA["O-FTRate"] * teamA["FTPct"] / (100**2)
        shooting_factor_B = teamB["O-FTRate"] * teamB["FTPct"] / (100**2)
        rebounding_factor_A = self.predict_rebounding_factor(teamA, teamB)
        rebounding_factor_B = self.predict_rebounding_factor(teamB, teamA)
        turnover_factor_A = self.predict_turnover_factor(teamA, teamB)
        turnover_factor_B = self.predict_turnover_factor(teamB, teamA)
        tempo = max(teamA["AdjTempo"], teamB["AdjTempo"]) 
        # NOTE: We add the shooting factor instead of multiplying because one FT = 1 pt (not 2). FTA is not included in FGM/eFG
        expectation_A = (2+ shooting_factor_A) * tempo * (teamA["O-eFGPct"]/100) * turnover_factor_A * rebounding_factor_A
        # variance_A = expectation_A ** 2 - (turnover_factor_A * rebounding_factor_A)**2 * (2 + shooting_factor_A) * (teamA["O-eFGPct"]/100)
        # print(f"{teamNameA}\t{shooting_factor_A}\t{turnover_factor_A}\t{rebounding_factor_A}\t{expectation_A}")
        expectation_B = (2+shooting_factor_B) * tempo * (teamB["O-eFGPct"]/100) * turnover_factor_B * rebounding_factor_B
        # variance_B = expectation_B ** 2 - (turnover_factor_B * rebounding_factor_B)**2 * tempo * (2 + shooting_factor_B) * (teamB["O-eFGPct"]/100)
        # print(f"{teamNameB}\t{shooting_factor_B}\t{turnover_factor_B}\t{rebounding_factor_B}\t{expectation_B}")
        return f"{teamNameA}: {expectation_A}\r\nSTDDEV: {expectation_A ** (1/2)}\r\n{teamNameB}: {expectation_B}\r\nSTDDEV: {expectation_B ** (1/2)}\r\n"

    def predict_shooting_factor(self, teamA, teamB):
        team_A_offensive_efg = teamA["O-FTRate"] / 100
        team_B_defensive_efg = teamB["D-FTRate"] / 100
        return team_A_offensive_efg + team_B_defensive_efg - team_A_offensive_efg * team_B_defensive_efg

    def predict_turnover_factor(self, teamA, teamB):
        team_A_turnover_rate = teamA["O-TOPct"] / 100
        team_B_turnover_rate = teamB["D-TOPct"] / 100
        return (1-team_A_turnover_rate) + (1-team_B_turnover_rate) - (1-team_A_turnover_rate) * (1-team_B_turnover_rate)

    def predict_rebounding_factor(self, teamA, teamB):
        team_A_rebounding_rate = teamA["O-ORPct"] / 100
        team_B_rebounding_rate = teamB["D-ORPct"] / 100
        return team_A_rebounding_rate + (1-team_B_rebounding_rate) - team_A_rebounding_rate * (1-team_B_rebounding_rate)

    def getOptions(self) -> list[str]:
        return [i for i in self._data.columns]
    
    def make_histogram(self, stat: str):
        d = self._data[stat]
        bins = [i for i in range(floor(min(d)), ceil(max(d)))]
        plt.hist(d, bins=bins)
        plt.show()

if __name__ == "__main__":
    d = Data()
    method = ""
    try:
        method = argv[1]
    except IndexError:
        teamA = input("Team A:\r\n")
        teamB = input("Team B:\r\n")
        print(d.predict(teamA, teamB))

    if method == "hist":
        [print(o) for o in d.getOptions()]
        stat = input("Input a stat:\r\n")
        d.make_histogram(stat)

