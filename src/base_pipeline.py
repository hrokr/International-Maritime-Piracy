import os
import re
import pandas as pd

data_directory = os.path.join("../data", "RAW_ASAM.csv")


def dms2dd(dms: str) -> int:
    """
    Converts latitude or longitude to decimal degrees 0°51'56.29"S
    """
    degrees, minutes, seconds, direction = re.split("[°'\"]+", dms)
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction in ("S", "W"):
        dd *= -1
    return dd


def main():
    df = pd.read_csv(data_directory)

    df.drop(["Unnamed: 8"], axis=1, inplace=True)

    df = df.join(df["position"].str.split(expand=True)).rename(
        columns={0: "latitude", 1: "longitude"}
    )
    df.drop("position", axis=1, inplace=True)

    df["latitude"] = df["latitude"].apply(dms2dd).round(6)
    df["longitude"] = df["longitude"].apply(dms2dd).round(6)

    df.fillna("No information", inplace=True)
    df.isnull().sum().sum()

    df.to_csv("../data/plumbed.csv")


if __name__ == "__main__":
    main()
