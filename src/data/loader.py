from pathlib import Path
import pandas as pd

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[2] / 'data' / 'raw' / 'aquisicoes-medicas-2025.csv'


def load_bps(path=DEFAULT_DATA_PATH):
    return pd.read_csv(path, sep=None, engine='python', encoding='utf-8')
