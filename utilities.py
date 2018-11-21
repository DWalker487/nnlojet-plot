import pandas as pd


def load_NNLOJET_file(infile):
    """ Reads in NNLOJET file <infile> and returns a formatted
    dataframe with the contents of the file."""
    df = pd.read_csv(infile, sep=" ", header=0, skipfooter=1)
    df.columns = df.columns[1:].append(pd.Index(["IGNORE"]))
    df.columns = pd.Index(i.split("[")[0] for i in df.columns)
    leading_column = df.columns[0]
    df = df[~df[leading_column].str.contains('\#')]
    df.drop("IGNORE", 1, inplace=True)
    df = df.reset_index(drop=True)
    df = df.apply(pd.to_numeric)
    df["scale_up"] = df[df.columns[3:17:2]].max(axis=1)
    df["scale_down"] = df[df.columns[3:17:2]].min(axis=1)
    return df
