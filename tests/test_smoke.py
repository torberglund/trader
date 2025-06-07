import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from strategies import ma_crossover_signal
import pandas as pd

def test_import():
    df = pd.DataFrame({'close': [1, 2, 3, 4, 5]})
    assert ma_crossover_signal(df) is None
