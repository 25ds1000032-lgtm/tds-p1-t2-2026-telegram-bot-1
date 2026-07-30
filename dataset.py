import os
import zipfile
import requests
import pandas as pd
from io import BytesIO


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
        filename = "dataset"

    filepath = os.path.join(
        DOWNLOAD_DIR,
        filename
    )

    with open(
        filepath,
        "wb"
    ) as f:
        f.write(response.content)

    return filepath



def extract_zip(filepath):
    """
    Extract ZIP files.
    """

    extract_path = filepath.replace(
        ".zip",
        ""
    )

    os.makedirs(
        extract_path,
        exist_ok=True
    )

    with zipfile.ZipFile(filepath) as z:
        z.extractall(extract_path)

    return extract_path



def load_dataset(filepath):
    """
    Load CSV or Excel dataset.
    """

    if filepath.endswith(".csv"):

        return pd.read_csv(filepath)


    if filepath.endswith(".xlsx") or filepath.endswith(".xls"):

        return pd.read_excel(filepath)


    raise ValueError(
        "Unsupported file format"
    )



def analyze_dataset(filepath):
    """
    Generate dataset summary.
    """

    if filepath.endswith(".zip"):

        filepath = extract_zip(filepath)

        files = []

        for root, _, filenames in os.walk(filepath):

            for name in filenames:

                if name.endswith(
                    (".csv", ".xlsx", ".xls")
                ):
                    files.append(
                        os.path.join(root, name)
                    )

        if not files:
            raise ValueError(
                "No dataset file found"
            )

        filepath = files[0]


    df = load_dataset(filepath)


    summary = {

        "rows": len(df),

        "columns": list(df.columns),

        "missing_values":
            df.isnull()
            .sum()
            .to_dict(),

        "data_types":
            df.dtypes
            .astype(str)
            .to_dict(),

        "numeric_summary":
            df.describe()
            .to_dict()

    }


    return summary