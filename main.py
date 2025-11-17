from data import Data

def main():
    data = Data("summary26.csv", _siz=50)
    print(f"Axis options")
    for s in data.getOptions(): print(s)
    xaxis=input("Input an axis:\n")
    yaxis=input("Input an axis:\n")
    data(_xaxis=xaxis, _yaxis=yaxis)

if __name__ == "__main__":
    main()
