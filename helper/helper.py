# Helper functions for notebooks
# Must be run from main directory due to relative file calls

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def loc_comm_df(loc, comm, vari=None):
    # Get a dataframe by commodity and location, sorted by year
    
    # raw data
    df_raw = pd.read_csv("data_raw/all_commodities.csv")

    # filter by location
    df = df_raw.loc[df_raw["Location"] == loc]
    assert(not df.empty), f"The loc value returned nothing, try {df_raw['Location'].unique()}"
    
    # filter by commodity
    df = df.loc[df["Commodity"] == str(comm)]
    assert(not df.empty), f"The comm value returned nothing, try {df_raw[df_raw['Location'] == loc]['Commodity'].unique()}"

    # If vari is specified, sort by variety
    if vari:
        df = df.loc[df["Variety"] == vari]
        assert(not df.empty), f"The vari value returned nothing, either remove it or try {(df_raw[(df_raw['Location'] == loc) & (df_raw['Commodity'] == comm)])['Variety'].unique()}"
    
    # sort by year, assert there are no duplicate years
    df = df.sort_values(by=["Item Year"])
    assert(len(df) == len(df["Item Year"].unique())), f"There are duplicate years. Here are the varieties: {df['Variety'].unique()}"
    
    return df


def miss_years(comm_loc_df):
    # Returns the missing years in a commodity and location dataframe, or if empty returns str 'none'
    # Assumes years are unique in given df and sorted (ascending)
    df_f_l = comm_loc_df["Item Year"].iloc[[0,-1]] # first and last year
    year_s = pd.Series(np.arange(df_f_l.iloc[0], df_f_l.iloc[-1]+1)) # full list from first to last year
    missing = pd.concat([comm_loc_df["Item Year"], year_s]).drop_duplicates(keep=False) # The missing years
    if missing.empty:
        missing = "none"
    else:
        missing = missing.tolist()
    return missing


def df_plot(df_comm_loc):
    # Returns a plot of a commodity and location dataframe

    # values for plot title and axes
    commodity = df_comm_loc["Commodity"].unique()
    location = df_comm_loc["Location"].unique()
    first_year = df_comm_loc["Item Year"].iloc[0]
    last_year = df_comm_loc["Item Year"].iloc[-1]
    measure = df_comm_loc["Standard Measure"].unique()

    # build plot objects
    fig, ax = plt.subplots()
    ax.plot(df_comm_loc["Item Year"], df_comm_loc["Standard Value"])
    ax.set(
        xlabel='year', 
        ylabel=f'price (silver standard / {measure[0]})',
        title=f'{commodity[0]} Prices in {location[0]} from {first_year} to {last_year}'
        )
    
    return fig, ax


if __name__ == '__main__':
    df = loc_comm_df("England", "Wheat", vari="asdf")
    #print(miss_years(df))
    fig, ax = df_plot(df)
