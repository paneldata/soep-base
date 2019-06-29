# -*- coding: utf-8 -*-

""" Helper functions for preprocessing pipeline """

import pathlib
from typing import List

import pandas as pd


def link_to(origin: str, target: str) -> None:
    """ Creates a symlink from origin to target """
    try:
        pathlib.Path(target).symlink_to(pathlib.Path(origin))
    except FileExistsError:
        pass


def add_columns(df: pd.DataFrame, columns: List[str]) -> None:
    """ Add columns to a DataFrame from a list of column names """
    for column in columns:
        df[column] = None


def extract_unique_values(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """ Extract the unique values of a given column name in a DataFrame """
    unique_values = df[column_name].dropna().unique()
    unique_values = pd.DataFrame(unique_values, columns=["name"])
    add_columns(unique_values, ["label", "label_de", "description"])
    unique_values.sort_values(by="name", inplace=True)
    return unique_values
