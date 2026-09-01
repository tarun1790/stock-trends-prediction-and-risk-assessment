"""
Unit Tests for Preprocessing and Data Representation Engine.
"""

import numpy as np
import pandas as pd
import pytest
from stock_predict.core.indicators import compute_all_indicators
from stock_predict.core.preprocessing import (
    continuous_preprocessing,
    binary_preprocessing,
    generate_target_labels,
    create_sequences,
    prepare_dataset,
    INDICATOR_COLUMNS,
)
from stock_predict.data.sample_data import generate_sector_historical_data


@pytest.fixture
def sample_data():
    return generate_sector_historical_data(num_days=200, seed=42)


def test_continuous_preprocessing(sample_data):
    ind_df = compute_all_indicators(sample_data).dropna()
    normalized, scaler = continuous_preprocessing(ind_df, INDICATOR_COLUMNS)

    assert normalized.shape == (len(ind_df), 10)
    assert np.all(normalized >= 0.0 - 1e-6)
    assert np.all(normalized <= 1.0 + 1e-6)


def test_binary_preprocessing(sample_data):
    ind_df = compute_all_indicators(sample_data).dropna()

    # Zero-one mode
    bin_01 = binary_preprocessing(ind_df, zero_one_mode=True)
    assert bin_01.shape == (len(ind_df), 10)
    unique_vals_01 = np.unique(bin_01)
    assert set(unique_vals_01).issubset({0.0, 1.0})

    # Paper mode {-1, +1}
    bin_pm = binary_preprocessing(ind_df, zero_one_mode=False)
    assert bin_pm.shape == (len(ind_df), 10)
    unique_vals_pm = np.unique(bin_pm)
    assert set(unique_vals_pm).issubset({-1.0, 1.0})


def test_create_sequences():
    X = np.random.randn(100, 10)
    y = np.random.randint(0, 2, size=100)
    seq_len = 15

    X_seq, y_seq = create_sequences(X, y, sequence_length=seq_len)
    assert X_seq.shape == (100 - seq_len + 1, seq_len, 10)
    assert y_seq.shape == (100 - seq_len + 1,)


def test_prepare_dataset(sample_data):
    cont_dict = prepare_dataset(sample_data, mode="continuous", sequence_length=10)
    assert "X_train" in cont_dict
    assert "X_test" in cont_dict
    assert "X_seq_train" in cont_dict
    assert "y_seq_train" in cont_dict

    bin_dict = prepare_dataset(sample_data, mode="binary", sequence_length=10)
    assert "X_train" in bin_dict
    assert set(np.unique(bin_dict["X_train"])).issubset({0.0, 1.0})
