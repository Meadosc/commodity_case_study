# Helper functions for notebooks
# Must be run from main directory due to relative file calls

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def comm_loc_df(comm, loc, vari=None):
    # Get a dataframe by commodity and location, sorted by year
    # Note: this function is space inefficient. Room for improvement.
    
    # raw data
    df_raw = pd.read_csv("data_raw/all_commodities.csv")

    # filter by commodity
    df_comm = df_raw.loc[df_raw["Commodity"] == str(comm)]
    assert(not df_comm.empty), f"The comm value returned nothing, try {df_raw['Commodity'].unique()}"

    # filter by location
    df_comm_loc = df_comm.loc[df_comm["Location"] == loc]
    assert(not df_comm_loc.empty), f"The loc value returned nothing, try {df_comm['Location'].unique()}"

    # If vari is specified, sort by variety
    if vari:
        df_comm_loc_vari = df_comm_loc.loc[df_comm["Variety"] == vari]
        assert(not df_comm_loc_vari.empty), f"The vari value returned nothing, either remove it or try {df_comm_loc['Variety'].unique()}"
    else:
        df_comm_loc_vari = df_comm_loc
    
    # sort by year, assert there are no duplicate years
    df_comm_loc_vari = df_comm_loc_vari.sort_values(by=["Item Year"])
    assert(len(df_comm_loc_vari) == len(df_comm_loc_vari["Item Year"].unique())), f"There are duplicate years. Here are the varieties: {df_comm_loc_vari['Variety'].unique()}"
    
    return df_comm_loc_vari


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
    df = comm_loc_df("Wheat", "England")
    #print(miss_years(df))
    fig, ax = df_plot(df)
