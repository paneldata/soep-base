import pathlib
import shutil

from ddi.onrails.repos import convert_r2ddi, copy, dor1

STUDY = "soep-base"
VERSION = "v1"

INPUT_DIRECTORY = pathlib.Path("metadata")
OUTPUT_DIRECTORY = pathlib.Path("ddionrails")


def main():
    copy.study()
    dor1.datasets()
    dor1.variables()
    convert_r2ddi.Parser(STUDY, version=VERSION).write_json()
    shutil.copy(
        INPUT_DIRECTORY.joinpath("analysis_units.csv"),
        OUTPUT_DIRECTORY.joinpath("analysis_units.csv"),
    )
    shutil.copy(
        INPUT_DIRECTORY.joinpath("concepts.csv"),
        OUTPUT_DIRECTORY.joinpath("concepts.csv"),
    )
    shutil.copy(
        INPUT_DIRECTORY.joinpath("conceptual_datasets.csv"),
        OUTPUT_DIRECTORY.joinpath("conceptual_datasets.csv"),
    )
    shutil.copy(
        INPUT_DIRECTORY.joinpath("periods.csv"),
        OUTPUT_DIRECTORY.joinpath("periods.csv"),
    )
    shutil.copy(
        INPUT_DIRECTORY.joinpath("publications.csv"),
        OUTPUT_DIRECTORY.joinpath("publications.csv"),
    )


if __name__ == "__main__":
    main()
