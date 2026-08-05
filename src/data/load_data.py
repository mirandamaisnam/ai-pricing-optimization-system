from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_datasets():

    data_path = PROJECT_ROOT / "data" / "raw"

    datasets = {}

    for file in data_path.glob("*.csv"):
        datasets[file.stem] = pd.read_csv(file)

    print(f"Loaded {len(datasets)} datasets successfully.")

    return datasets