# -*- coding: utf-8 -*-

""" Preprocessing pipeline for soep-base """

import pathlib

import pandas as pd
from ddi.onrails.repos import convert_r2ddi

from helpers import add_columns, extract_unique_values, link_to

STUDY = "soep-base"
VERSION = "v1"

INPUT_DIRECTORY = pathlib.Path("metadata")
OUTPUT_DIRECTORY = pathlib.Path("ddionrails")


def preprocess_datasets():
    """ Add columns to datasets.csv """
    datasets = pd.read_csv(INPUT_DIRECTORY.joinpath("datasets.csv"))
    add_columns(datasets, ["label", "label_de", "description"])
    wanted_columns = [
        "study",
        "name",
        "label",
        "label_de",
        "description",
        "analysis_unit",
        "conceptual_dataset",
        "period",
    ]
    datasets = datasets[wanted_columns]
    datasets.to_csv(OUTPUT_DIRECTORY.joinpath("datasets.csv"), index=False)


def run():
    # create symlinks
    link_to("../metadata/study.md", OUTPUT_DIRECTORY.joinpath("study.md"))
    link_to("../metadata/bibtex.bib", OUTPUT_DIRECTORY.joinpath("bibtex.bib"))
    link_to("../metadata/variables.csv", OUTPUT_DIRECTORY.joinpath("variables.csv"))

    # extract related objects from datasets
    datasets = pd.read_csv(INPUT_DIRECTORY.joinpath("datasets.csv"))
    analysis_units = extract_unique_values(datasets, "analysis_unit")
    conceptual_datasets = extract_unique_values(datasets, "conceptual_dataset")
    periods = extract_unique_values(datasets, "period")
    periods.insert(loc=0, column="study", value=STUDY)
    periods.insert(loc=len(periods.columns), column="definition", value=None)
    analysis_units.to_csv(OUTPUT_DIRECTORY.joinpath("analysis_units.csv"), index=False)
    conceptual_datasets.to_csv(
        OUTPUT_DIRECTORY.joinpath("conceptual_datasets.csv"), index=False
    )
    periods.to_csv(OUTPUT_DIRECTORY.joinpath("periods.csv"), index=False)

    # extract related objects from variables
    variables = pd.read_csv(INPUT_DIRECTORY.joinpath("variables.csv"))
    concepts = extract_unique_values(variables, "concept")
    concepts.insert(loc=len(concepts.columns), column="topic", value=None)
    concepts.to_csv(OUTPUT_DIRECTORY.joinpath("concepts.csv"), index=False)

    # preprocessing
    preprocess_datasets()
    convert_r2ddi.Parser(STUDY, version=VERSION).write_json()


if __name__ == "__main__":
    run()
