import pandas as pd
import re


def preprocess(df):
    df.dropna(subset=["description"], inplace=True)
    df.dropna(axis=1, how="all", inplace=True)
    df.fillna("No information", inplace=True)

    return df


def splitLatLong(df: str) -> str:
    df = df.join(df["position"].str.split(expand=True)).rename(
        columns={0: "latitude", 1: "longitude"}
    )
    df.drop("position", axis=1, inplace=True)

    return df


def dms2dd(field):
    degrees, minutes, seconds, direction = re.split('[°\'"]+', field)

    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction in ("S", "W"):
        dd *= -1
    return dd

def conv_to_dd(df):
    print("made it the conversion function")
    
    df["latitude"] = df["latitude"].apply(dms2dd)
    df["longitude"] = df["longitude"].apply(dms2dd)

    print("three for three, baby!")
    return df


# df.isnull().sum().sum()


# # And now save it as a new file
# df.to_csv('../data/step2.csv', sep='|', encoding='utf-8')
# print("file cleaned")
