import re
import pandas as pd


def preprocess(df):
    """
    preprocesses csv by:
        Drop columns with no event description (critical issue)
        Drop columns where all values are NaN (i.e., 'Unnamed: 8')
        Change NaN values to 'No Information' (critical issue)
        Convert date column to datetime (used for index)
    """

    df.dropna(subset=["description"], inplace=True)
    df.dropna(axis=1, how="all", inplace=True)
    df.fillna("No information", inplace=True)
    df["date"] = pd.to_datetime(df["date"])

    return df


def splitLatLong(df):
    """
    Converts the 'position' column into separate columns ('latitude' and 'longitude')
    Removes  the 'position' column.
    """

    df = df.join(df["position"].str.split(expand=True)).rename(
        columns={0: "latitude", 1: "longitude"}
    )
    df.drop("position", axis=1, inplace=True)

    return df


def dms2dd(field) -> float:
    """
    Converts postition from Degrees, Minutes, Seconds (DMS) to decimal degrees.
    """

    degrees, minutes, seconds, direction = re.split("[°'\"]+", field)
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction in ("S", "W"):
        dd *= -1

    return dd


def conv_to_dd(df):
    """
    Sends latitude and longitude columns to dms2dd function for conversion to
    decimal degrees.
    """

    df["latitude"] = df["latitude"].apply(dms2dd)
    df["longitude"] = df["longitude"].apply(dms2dd)

    return df


def baseline_processing(df):
    preprocess(df)
    df = splitLatLong(df)
    df = conv_to_dd(df)
    print("Preprocessing completed")

    return df


def export_as_pickle(df):
    df.to_pickle("../data/in_progress/pickled_data.pkl")
