import os

import pandas as pd

from csv_processor import baseline_processing, export_as_pickle, fix_references

data_directory = os.path.join("../data", "RAW_ASAM.csv")
df = pd.read_csv(data_directory, skipinitialspace=True)


if __name__ == "__main__":

    df = baseline_processing(df)
    df = fix_references(df)
    print(df)

    os.makedirs("../data/in_progress", exist_ok=True)
    export_as_pickle(df)
