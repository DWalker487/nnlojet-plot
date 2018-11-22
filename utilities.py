import pandas as pd
import numpy as np


def load_NNLOJET_file(infile):
    """ Reads in NNLOJET file <infile> and returns a formatted
    dataframe with the contents of the file."""
    df = pd.read_csv(infile, sep=" ", header=0, skipfooter=1, engine='python')
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


def ratio_NNLOJET_files(numerator, denominator):
    # Check all columns are the same in both dataframes
    assert all(numerator.columns == denominator.columns)
    # Check all rows are the same in both dataframes
    assert all(numerator.index.values == denominator.index.values)

    df = pd.DataFrame(index=numerator.index.values,
                      columns=numerator.columns)
    df[df.columns[:3]] = numerator[df.columns[:3]]
    for val_column in df.columns[3:-2:2]:
        df[val_column] = numerator[val_column]/denominator[val_column]
    for err_column in df.columns[4:-2:2]:
        val_column = df.columns[[df.columns.get_loc(err_column)-1]][0]
        # Combine stat errors
        df[err_column] = numerator[val_column]/denominator[val_column]\
                         *np.sqrt((numerator[err_column]/numerator[val_column])**2\
                                  +(denominator[err_column]/denominator[val_column])**2)

    # For now, use numerator scale errors normalised to denominator central scale
    df["scale_up"] = numerator["scale_up"]/denominator["tot_scale01"]
    df["scale_down"] = numerator["scale_down"]/denominator["tot_scale01"]
    return df
