import os
import zipfile
import requests
import pandas as pd


DOWNLOAD_DIR = "datasets"


def download_file(url):
    """
    Download dataset from URL.
    """

    os.makedirs(
        DOWNLOAD_DIR,
        exist_ok=True
    )

    response = requests.get(
        url,
        timeout=60
    )

    response.raise_for_status()

    filename = url.split("/")[-1]

    if not filename:
        filename = "dataset.csv"

    filepath = os.path.join(
        DOWNLOAD_DIR,
        filename
    )

    with open(
        filepath,
        "wb"
    ) as f:
        f.write(
            response.content
        )

    return filepath



def extract_zip(filepath):
    """
    Extract zip file.
    """

    extract_dir = filepath.replace(
        ".zip",
        ""
    )

    os.makedirs(
        extract_dir,
        exist_ok=True
    )

    with zipfile.ZipFile(filepath) as z:

        z.extractall(
            extract_dir
        )

    return extract_dir



def load_dataset(filepath):
    """
    Load CSV or Excel file.
    """

    if filepath.endswith(".csv"):

        return pd.read_csv(
            filepath
        )

    elif filepath.endswith(
        (".xlsx", ".xls")
    ):

        return pd.read_excel(
            filepath
        )

    else:

        raise ValueError(
            "Unsupported dataset format"
        )



def analyze_dataset(filepath):
    """
    Generate dataset summary for LLM.
    """

    if filepath.endswith(".zip"):

        filepath = extract_zip(
            filepath
        )

        files = []

        for root, _, filenames in os.walk(filepath):

            for name in filenames:

                if name.lower().endswith(
                    (
                        ".csv",
                        ".xlsx",
                        ".xls"
                    )
                ):

                    files.append(
                        os.path.join(
                            root,
                            name
                        )
                    )


        if not files:

            raise ValueError(
                "No supported dataset found in ZIP"
            )


        filepath = files[0]


    df = load_dataset(
        filepath
    )


    numeric_summary = {}

    numeric_df = df.select_dtypes(
        include="number"
    )

    if not numeric_df.empty:

        numeric_summary = (
            numeric_df
            .describe()
            .fillna("")
            .to_dict()
        )


    categorical_summary = {}

    for col in df.select_dtypes(
        exclude="number"
    ).columns[:10]:

        categorical_summary[col] = (
            df[col]
            .astype(str)
            .value_counts()
            .head(10)
            .to_dict()
        )


    summary = {

        "file": filepath,

        "rows": len(df),

        "columns": list(df.columns),

        "data_types":
            df.dtypes.astype(str).to_dict(),

        "missing_values":
            df.isnull().sum().to_dict(),

        "duplicate_rows":
            int(df.duplicated().sum()),

        "head":
            df.head(10)
            .fillna("")
            .to_dict(
                orient="records"
            ),

        "numeric_summary":
            numeric_summary,

        "categorical_summary":
            categorical_summary

    }


    return summary