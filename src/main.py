import os

import pandas as pd
from csv_processor import baseline_processing, fix_references

data_directory = os.path.join("../data", "RAW_ASAM.csv")
df = pd.read_csv(data_directory, skipinitialspace=True)


if __name__ == "__main__":

    baseline_processing(df)
    fix_references(df)
    print(df)

    os.makedirs("../data/in_progress", exist_ok=True)
    df.to_pickle("../data/in_progress/pickled.pkl")
