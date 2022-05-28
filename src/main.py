import os

import pandas as pd
from csv_processor import baseline_processing

data_directory = os.path.join("../data", "RAW_ASAM.csv")
df = pd.read_csv(data_directory)


if __name__ == "__main__":

    baseline_processing(df)
    print(df)

