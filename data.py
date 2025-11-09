import pandas as pd
import matplotlib.pyplot as plt

class Data:
    _data: pd.DataFrame
    _fname: str
    _siz: int

    def __init__(self, _fname: str, _siz=-1, _sort_axis_label="RankAdjEM"):
        self._fname = _fname
        self._data = pd.read_csv(self._fname)
        self._data = self._data.sort_values(_sort_axis_label, ascending=True)
        self._siz = _siz

    def __call__(self):
        labels = list(self._data["TeamName"])
        x = list(self._data["AdjOE"])
        y = list(self._data["AdjDE"])

        if(self._siz != -1):
            labels = labels[:self._siz]
            x = x[:self._siz]
            y = y[:self._siz]

        plt.xlabel("Adjusted Offensive Efficiency")
        plt.ylabel("Adjusted Defensive Efficiency")
        plt.title("Offensive Efficiency (Adj) vs Defensive Efficiency (Adj) (KenPom Top 50)")
        plt.scatter(x, y)

        for i, txt in enumerate(labels):
            plt.text(x[i] + 0.1, y[i] + 0.2, txt, fontsize=9)

        plt.grid(True)
        plt.show()