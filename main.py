from data import Data
from sys import argv

def main():
    try:
        data = Data("./data/summary26.csv", int(argv[1]))
    except IndexError:
        data = Data("./data/summary26.csv")
    print(f"Axis options")
    for s in data.getOptions(): print(s)
    xaxis=input("Input an axis:\n")
    yaxis=input("Input an axis:\n")
    data(_xaxis=xaxis, _yaxis=yaxis)

if __name__ == "__main__":
    main()
