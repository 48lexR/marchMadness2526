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

    def __call__(self, _xaxis = "AdjOE", _yaxis = "AdjDE") -> None:
        labels = self._data["TeamName"]
        ranks = self._data["RankAdjEM"]
        x_vals = self._data[_xaxis]
        y_vals = self._data[_yaxis]

        if(self._siz != -1):
            labels = labels[:self._siz]
            ranks = ranks[:self._siz]
            x_vals = x_vals[:self._siz]
            y_vals = y_vals[:self._siz]

        plt.xlabel(_xaxis)
        plt.ylabel(_yaxis)
        plt.title("Offensive Efficiency (Adj) vs Defensive Efficiency (Adj) (KenPom Top 50)")
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

    def getOptions(self) -> list[str]:
        return [i for i in self._data.columns]
            