import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from strategies import ma_crossover_signal, combined_signal
import pandas as pd

def test_import():
    df = pd.DataFrame(
        {
            'close': [1, 2, 3, 4, 5],
            'high': [1, 2, 3, 4, 5],
            'low': [1, 1, 2, 3, 4]
        },
        index=pd.date_range("2020-01-01", periods=5, freq="D")
    )
    sig1 = ma_crossover_signal(df)
    assert sig1 is None or hasattr(sig1, "action")
    sig = combined_signal(df)
    assert sig is None or hasattr(sig, "action")
