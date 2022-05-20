import difflib
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
    degrees, minutes, seconds, direction = re.split("[°'\"]+", field)
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction in ("S", "W"):
        dd *= -1

    return dd


def conv_to_dd(df):

    df["latitude"] = df["latitude"].apply(dms2dd)
    df["longitude"] = df["longitude"].apply(dms2dd)
    print("file cleaned")

    return df


def baseline_processing(df):
    preprocess(df)
    df = splitLatLong(df)
    df = conv_to_dd(df)

    return df