"""
Preprocessing & Data Representation Engine.
Implements Continuous Normalization [0, 1] and Trend Deterministic Binary Transformation (+1 / -1)
as detailed in Section II-B of the IEEE Access paper.
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from stock_predict.config import PreprocessingConfig
from stock_predict.core.indicators import compute_all_indicators

INDICATOR_COLUMNS = [
    "SMA", "WMA", "MOM", "STCK", "STCD", "RSI", "SIG", "LWR", "ADO", "CCI"
]


def generate_target_labels(df: pd.DataFrame, close_col: str = "Close") -> pd.Series:
    """
    Generate target stock movement direction for day t+1:
    y_t = 1 (Up) if Close_{t+1} > Close_t else 0 (Down).
    """
    next_close = df[close_col].shift(-1)
    target = (next_close > df[close_col]).astype(int)
    return target


def continuous_preprocessing(
    df: pd.DataFrame,
    feature_cols: Optional[List[str]] = None,
    scaler: Optional[MinMaxScaler] = None,
    fit_scaler: bool = True,
) -> Tuple[np.ndarray, MinMaxScaler]:
    """
    Normalize technical indicators to range [0, 1] using MinMax scaling.

    Args:
        df: DataFrame containing the indicator columns.
        feature_cols: List of feature column names (defaults to 10 indicators).
        scaler: Existing MinMaxScaler instance (optional).
        fit_scaler: Whether to fit the scaler on the input data.

    Returns:
        Tuple of (normalized numpy array, fitted MinMaxScaler).
    """
    cols = feature_cols or INDICATOR_COLUMNS
    features = df[cols].values.astype(np.float64)

    if scaler is None:
        scaler = MinMaxScaler(feature_range=(0, 1))

    if fit_scaler:
        normalized = scaler.fit_transform(features)
    else:
        normalized = scaler.transform(features)

    # Handle any NaN/Inf
    normalized = np.nan_to_num(normalized, nan=0.5, posinf=1.0, neginf=0.0)
    return normalized, scaler


def binary_preprocessing(
    df: pd.DataFrame,
    close_col: str = "Close",
    zero_one_mode: bool = True,
) -> np.ndarray:
    """
    Convert continuous technical indicators to Trend-Deterministic Binary signals
    based on the exact domain rules from Section II-B of the paper:

    - SMA:  +1 if Close_t >= SMA_t else -1
    - WMA:  +1 if Close_t >= WMA_t else -1
    - MOM:  +1 if MOM_t > 0 else -1
    - STCK: +1 if STCK_t > STCK_{t-1} else -1
    - STCD: +1 if STCD_t > STCD_{t-1} else -1
    - LWR:  +1 if LWR_t > LWR_{t-1} else -1
    - SIG:  +1 if SIG_t > SIG_{t-1} else -1
    - ADO:  +1 if ADO_t > ADO_{t-1} else -1
    - RSI:  -1 if RSI_t > 70, +1 if RSI_t < 30, else (+1 if RSI_t > RSI_{t-1} else -1)
    - CCI:  -1 if CCI_t > 200, +1 if CCI_t < -200, else (+1 if CCI_t > CCI_{t-1} else -1)

    Args:
        df: DataFrame containing price and indicator columns.
        close_col: Name of close price column.
        zero_one_mode: If True, maps {-1, +1} to {0, 1} for classification compatibility.

    Returns:
        2D numpy array of shape (N, 10) containing binary signals.
    """
    close = df[close_col]
    binary_df = pd.DataFrame(index=df.index)

    # SMA & WMA
    binary_df["SMA"] = np.where(close >= df["SMA"], 1, -1)
    binary_df["WMA"] = np.where(close >= df["WMA"], 1, -1)

    # MOM
    binary_df["MOM"] = np.where(df["MOM"] > 0, 1, -1)

    # STCK, STCD, LWR, SIG, ADO (Diff > 0 -> +1, else -1)
    for col in ["STCK", "STCD", "LWR", "SIG", "ADO"]:
        diff = df[col].diff()
        binary_df[col] = np.where(diff > 0, 1, -1)

    # RSI
    rsi = df["RSI"]
    rsi_diff = rsi.diff()
    rsi_binary = np.where(
        rsi > 70,
        -1,
        np.where(
            rsi < 30,
            1,
            np.where(rsi_diff > 0, 1, -1)
        )
    )
    binary_df["RSI"] = rsi_binary

    # CCI
    cci = df["CCI"]
    cci_diff = cci.diff()
    cci_binary = np.where(
        cci > 200,
        -1,
        np.where(
            cci < -200,
            1,
            np.where(cci_diff > 0, 1, -1)
        )
    )
    binary_df["CCI"] = cci_binary

    binary_array = binary_df[INDICATOR_COLUMNS].values.astype(np.float32)

    if zero_one_mode:
        # Convert -1 to 0, +1 stays 1
        binary_array = np.where(binary_array == 1, 1.0, 0.0)

    return binary_array


def create_sequences(
    X: np.ndarray, y: np.ndarray, sequence_length: int = 20
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Transform 2D features into 3D sliding-window sequences for Recurrent and Attention architectures.
    Input shape: (N, Features)
    Output shape: (N - sequence_length + 1, sequence_length, Features)
    Target shape: (N - sequence_length + 1,) matching the trend after the sequence window.
    """
    if len(X) < sequence_length:
        raise ValueError(
            f"Dataset length ({len(X)}) is smaller than sequence length ({sequence_length})"
        )

    num_samples = len(X) - sequence_length + 1
    num_features = X.shape[1]

    X_seq = np.zeros((num_samples, sequence_length, num_features), dtype=np.float32)
    y_seq = np.zeros(num_samples, dtype=np.int64)

    for i in range(num_samples):
        X_seq[i] = X[i : i + sequence_length]
        y_seq[i] = y[i + sequence_length - 1]

    return X_seq, y_seq


def prepare_dataset(
    df: pd.DataFrame,
    mode: str = "continuous",
    sequence_length: Optional[int] = None,
    test_size: float = 0.30,
    random_split: bool = False,
    random_state: int = 42,
) -> Dict[str, Union[np.ndarray, MinMaxScaler, pd.DataFrame]]:
    """
    Full end-to-end dataset preparation pipeline.

    1. Computes all 10 technical indicators.
    2. Drops initial warmup NaN rows and the final row (shifted target).
    3. Transforms features into Continuous [0, 1] or Binary {0, 1}.
    4. Splits into Train / Test sets (Chronological time-series split or Random split).
    5. Optionally creates 3D sequences for deep learning models.

    Args:
        df: Raw OHLCV DataFrame.
        mode: 'continuous' or 'binary'.
        sequence_length: Lookback window length (e.g. 20). If provided, also returns 3D tensors.
        test_size: Proportion for test split (default 0.30 as in paper).
        random_split: If True, uses random train_test_split (paper evaluation), else chronological.
        random_state: Random seed.

    Returns:
        Dictionary with X_train, X_test, y_train, y_test, (and sequence versions if requested).
    """
    # 1. Compute indicators
    ind_df = compute_all_indicators(df)

    # 2. Target labeling
    close_col = "Close" if "Close" in ind_df.columns else "close"
    ind_df["Target"] = generate_target_labels(ind_df, close_col=close_col)

    # Drop NaN rows from indicator warmup window and last row (target shift NaN)
    clean_df = ind_df.dropna().copy()
    clean_df = clean_df.iloc[:-1].copy()

    # 3. Feature transformation
    scaler = None
    if mode == "binary":
        X = binary_preprocessing(clean_df, close_col=close_col, zero_one_mode=True)
    else:
        X, scaler = continuous_preprocessing(clean_df, feature_cols=INDICATOR_COLUMNS)

    y = clean_df["Target"].values.astype(np.int64)

    # 4. Train / Test Split
    n_samples = len(X)
    split_idx = int(n_samples * (1.0 - test_size))

    if random_split:
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, shuffle=True
        )
    else:
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

    data_dict: Dict[str, Union[np.ndarray, MinMaxScaler, pd.DataFrame]] = {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "raw_df": clean_df,
        "scaler": scaler,
        "mode": mode,
    }

    # 5. Sequences for recurrent DL
    if sequence_length and sequence_length > 1:
        X_seq, y_seq = create_sequences(X, y, sequence_length=sequence_length)
        seq_split_idx = int(len(X_seq) * (1.0 - test_size))
        if random_split:
            from sklearn.model_selection import train_test_split
            X_seq_train, X_seq_test, y_seq_train, y_seq_test = train_test_split(
                X_seq, y_seq, test_size=test_size, random_state=random_state, shuffle=True
            )
        else:
            X_seq_train, X_seq_test = X_seq[:seq_split_idx], X_seq[seq_split_idx:]
            y_seq_train, y_seq_test = y_seq[:seq_split_idx], y_seq[seq_split_idx:]

        data_dict["X_seq_train"] = X_seq_train
        data_dict["X_seq_test"] = X_seq_test
        data_dict["y_seq_train"] = y_seq_train
        data_dict["y_seq_test"] = y_seq_test

    return data_dict
