import pandas as pd
import re


# Parse regexed files.

def dewonk(file):
    print(f"Removing stray newlines in {file}")
    return re.sub(r"(?<=[/w])\n+(?=[/w])",'', file)


def to_list(filename):
    with open(filename) as file:
        print(f"Converting {filename} items to list")
        return [term.replace('\n', '')for term in file]


def to_nested_lists(inlist, file_out):
    nested_list = []
    sublist = []
    while len(inlist) > 0:
        sublist = list(inlist[0:7])
        nested_list.append(sublist)
        del inlist[0:7] 
    data = pd.DataFrame(nested_list)
    file_out = "datac.csv"
    data.to_csv(file_out, index=False, header=False)
    print(f"Converting {inlist} from list to nested lists")
    print(f"Done! {file_out} was made ")


# Conversion from Degrees(º), Min('), Sec(") to decimal degrees (eg, 23.4988858)

def deg_min_sec_to_dd(deg: int, min: int, sec: int, dir: str) -> float:
    multiplier = 1 if (dir == "N" or dir == "E") else -1
    return (deg + min/60 + sec/3600) * multiplier


def long_for_pandas(LongDeg, LongMin, LongSec, LongDir):
    Direction = 1
    LongDeg = row["LongDeg"]
    LongMin = row["LongMin"]
    LongSec = row["LongSec"]
    LongDir = row["LongDir"]
    if LongDir == "W":
        Direction = -1

    multiplier = 1 if LongDir == "E" else -1
    return LongDeg + LongMin/60 + LongSec/3600 * multiplier


def lat_for_pandas(LatDeg, LatMin, LatSec, LatDir):
    Direction = 1
    LatDeg = row["LatDeg"]
    LatMin = row["LatMin"]
    LatSec = row["LatSec"]
    LatDir = row["LatDiat"]

    if LatDir == "W":
        Direction = -1

    multiplier = 1 if LatDir == "E" else -1
    return LatDeg + LatMin/60 + LatSec/3600 * multiplier






if __name__ == "__main__":

    #def Long(row)

# Parse
    # dewonk = dewonk("ASAM_clean_scrub.txt")

    # listed = to_list("ASAM_clean_scrub.txt")

    # print(ret_list)

    # cleaned = to_nested_lists(listed)

# Converstion
    # dd = deg_min_sec_to_dd(2, .34, 2, 3)

    # df["Lat"] = df.apply(lambda row: Lat(row), axis=1)

    # df["Long"] = df.apply(lambda row: Long(row), axis=1)
