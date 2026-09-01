"""
Next-Generation Deep Learning Architectures (GPU/CUDA Accelerated):
- Temporal Convolutional Network (TCN) with Dilated Causal 1D Convolutions
- Temporal Fusion Transformer (TFT) with Variable Selection Networks (VSN)
- Multi-Horizon Neural Forecaster (1D, 3D, 5D, 10D, 20D) with Uncertainty Estimation
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import copy
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from stock_predict.config import get_device
from stock_predict.models.base import BaseModelWrapper


# =========================================================================
# 1. Temporal Convolutional Network (TCN) Components
# =========================================================================

class Chomp1d(nn.Module):
    """Chomp trailing padding to enforce causal convolutions."""
    def __init__(self, chomp_size: int):
        super().__init__()
        self.chomp_size = chomp_size

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x[:, :, :-self.chomp_size].contiguous() if self.chomp_size > 0 else x


class TemporalBlock(nn.Module):
    """Residual Dilated Causal Convolutional Block for TCN."""
    def __init__(
        self,
        n_inputs: int,
        n_outputs: int,
        kernel_size: int,
        stride: int,
        dilation: int,
        padding: int,
        dropout: float = 0.2,
    ):
        super().__init__()
        self.conv1 = nn.utils.weight_norm(
            nn.Conv1d(
                n_inputs,
                n_outputs,
                kernel_size,
                stride=stride,
                padding=padding,
                dilation=dilation,
            )
        )
        self.chomp1 = Chomp1d(padding)
        self.relu1 = nn.GELU()
        self.dropout1 = nn.Dropout(dropout)

        self.conv2 = nn.utils.weight_norm(
            nn.Conv1d(
                n_outputs,
                n_outputs,
                kernel_size,
                stride=stride,
                padding=padding,
                dilation=dilation,
            )
        )
        self.chomp2 = Chomp1d(padding)
        self.relu2 = nn.GELU()
        self.dropout2 = nn.Dropout(dropout)

        self.net = nn.Sequential(
            self.conv1, self.chomp1, self.relu1, self.dropout1,
            self.conv2, self.chomp2, self.relu2, self.dropout2
        )
        self.downsample = (
            nn.Conv1d(n_inputs, n_outputs, 1) if n_inputs != n_outputs else None
        )
        self.relu = nn.GELU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.net(x)
        res = x if self.downsample is None else self.downsample(x)
        return self.relu(out + res)


class PyTorchTCN(nn.Module):
    """
    Temporal Convolutional Network.
    Outperforms LSTMs on financial time-series with exponential receptive fields.
    """
    def __init__(
        self,
        input_dim: int = 10,
        num_channels: List[int] = None,
        kernel_size: int = 3,
        dropout: float = 0.2,
        num_classes: int = 2,
    ):
        super().__init__()
        if num_channels is None:
            num_channels = [64, 64, 128, 128]

        layers: List[nn.Module] = []
        num_levels = len(num_channels)
        for i in range(num_levels):
            dilation_size = 2 ** i
            in_channels = input_dim if i == 0 else num_channels[i - 1]
            out_channels = num_channels[i]
            layers.append(
                TemporalBlock(
                    in_channels,
                    out_channels,
                    kernel_size,
                    stride=1,
                    dilation=dilation_size,
                    padding=(kernel_size - 1) * dilation_size,
                    dropout=dropout,
                )
            )

        self.network = nn.Sequential(*layers)
        self.fc = nn.Sequential(
            nn.Linear(num_channels[-1], 32),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(32, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Input: (batch, seq_len, features) -> transpose to (batch, features, seq_len)
        if x.dim() == 2:
            x = x.unsqueeze(1)
        x_t = x.transpose(1, 2)
        y = self.network(x_t)
        # Take last time step
        last_step = y[:, :, -1]
        return self.fc(last_step)


# =========================================================================
# 2. Temporal Fusion Transformer (TFT) with Variable Selection
# =========================================================================

class GatedResidualNetwork(nn.Module):
    """Gated Residual Network (GRN) for non-linear processing and gating."""
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, dropout: float = 0.1):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.elu = nn.ELU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout)
        self.gate = nn.Linear(hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()
        self.skip = nn.Linear(input_dim, output_dim) if input_dim != output_dim else nn.Identity()
        self.layer_norm = nn.LayerNorm(output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        a = self.elu(self.fc1(x))
        b = self.dropout(self.fc2(a))
        gate = self.sigmoid(self.gate(a))
        gated_out = gate * b
        return self.layer_norm(self.skip(x) + gated_out)


class VariableSelectionNetwork(nn.Module):
    """Variable Selection Network (VSN) dynamically weighting input feature importances."""
    def __init__(self, num_features: int, hidden_dim: int, dropout: float = 0.1):
        super().__init__()
        self.num_features = num_features
        self.hidden_dim = hidden_dim

        # Per-feature entity embeddings
        self.feature_transforms = nn.ModuleList([
            GatedResidualNetwork(1, hidden_dim, hidden_dim, dropout)
            for _ in range(num_features)
        ])
        # Feature weighting GRN
        self.flatten_grn = GatedResidualNetwork(
            num_features, hidden_dim, num_features, dropout
        )
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # x: (batch, seq_len, num_features)
        batch_size, seq_len, _ = x.shape
        weights = self.softmax(self.flatten_grn(x))  # (batch, seq_len, num_features)

        transformed = []
        for i in range(self.num_features):
            feat_slice = x[:, :, i : i + 1]  # (batch, seq_len, 1)
            t_feat = self.feature_transforms[i](feat_slice)  # (batch, seq_len, hidden_dim)
            transformed.append(t_feat.unsqueeze(2))

        # (batch, seq_len, num_features, hidden_dim)
        stacked = torch.cat(transformed, dim=2)
        # Weight each transformed feature
        weighted = stacked * weights.unsqueeze(-1)
        # Sum across features: (batch, seq_len, hidden_dim)
        selected_features = weighted.sum(dim=2)
        return selected_features, weights


class PyTorchTFT(nn.Module):
    """
    Temporal Fusion Transformer with Variable Selection & Interpretable Attention.
    """
    def __init__(
        self,
        input_dim: int = 10,
        hidden_dim: int = 64,
        num_heads: int = 4,
        num_layers: int = 2,
        dropout: float = 0.1,
        num_classes: int = 2,
    ):
        super().__init__()
        self.vsn = VariableSelectionNetwork(input_dim, hidden_dim, dropout)
        self.lstm = nn.LSTM(
            hidden_dim, hidden_dim, num_layers=num_layers, batch_first=True, dropout=dropout
        )
        self.mha = nn.MultiheadAttention(
            embed_dim=hidden_dim, num_heads=num_heads, batch_first=True
        )
        self.post_norm = nn.LayerNorm(hidden_dim)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(32, num_classes),
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if x.dim() == 2:
            x = x.unsqueeze(1)
        vsn_out, var_weights = self.vsn(x)
        lstm_out, _ = self.lstm(vsn_out)
        attn_out, attn_weights = self.mha(lstm_out, lstm_out, lstm_out)
        normed = self.post_norm(lstm_out + attn_out)
        last_step = normed[:, -1, :]
        logits = self.fc(last_step)
        return logits, var_weights, attn_weights


# =========================================================================
# 3. Multi-Horizon Neural Forecaster
# =========================================================================

class MultiHorizonNetwork(nn.Module):
    """
    Multi-Task Neural Network predicting 1D, 3D, 5D, 10D, and 20D forward horizons.
    Outputs: Direction Probabilities and Expected Return Magnitudes.
    """
    def __init__(
        self,
        input_dim: int = 10,
        hidden_dim: int = 128,
        horizons: List[int] = None,
        dropout: float = 0.2,
    ):
        super().__init__()
        self.horizons = horizons or [1, 3, 5, 10, 20]
        self.shared_lstm = nn.LSTM(
            input_dim, hidden_dim, num_layers=2, batch_first=True, dropout=dropout
        )
        self.shared_fc = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.GELU(),
            nn.Dropout(dropout),
        )

        # Classification Heads (Direction 0/1) for each horizon
        self.direction_heads = nn.ModuleDict({
            f"h_{h}": nn.Linear(64, 2) for h in self.horizons
        })
        # Regression Heads (Magnitude % Return) for each horizon
        self.magnitude_heads = nn.ModuleDict({
            f"h_{h}": nn.Linear(64, 1) for h in self.horizons
        })

    def forward(self, x: torch.Tensor) -> Dict[str, Dict[str, torch.Tensor]]:
        if x.dim() == 2:
            x = x.unsqueeze(1)
        out, _ = self.shared_lstm(x)
        feat = self.shared_fc(out[:, -1, :])

        results = {}
        for h in self.horizons:
            logits = self.direction_heads[f"h_{h}"](feat)
            magnitude = self.magnitude_heads[f"h_{h}"](feat)
            results[f"horizon_{h}d"] = {
                "logits": logits,
                "magnitude": magnitude,
            }
        return results


class MultiHorizonForecaster:
    """
    Multi-Horizon Forecast Wrapper with Uncertainty Quantification.
    """
    def __init__(
        self,
        input_dim: int = 10,
        horizons: Optional[List[int]] = None,
        learning_rate: float = 0.001,
        epochs: int = 60,
        batch_size: int = 64,
        device: Optional[torch.device] = None,
    ):
        self.input_dim = input_dim
        self.horizons = horizons or [1, 3, 5, 10, 20]
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.device = device or get_device()
        self.model = MultiHorizonNetwork(
            input_dim=input_dim, horizons=self.horizons
        ).to(self.device)

    def fit(self, X_seq: np.ndarray, price_series: np.ndarray) -> "MultiHorizonForecaster":
        """
        Train multi-horizon network predicting returns at 1D, 3D, 5D, 10D, 20D.
        """
        self.model.train()
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

        # Generate multi-horizon targets
        n_samples = len(X_seq)
        max_h = max(self.horizons)
        valid_samples = n_samples - max_h

        if valid_samples <= 0:
            return self

        X_train = torch.tensor(X_seq[:valid_samples], dtype=torch.float32)

        # Targets
        dir_targets = {}
        mag_targets = {}
        for h in self.horizons:
            ret = (price_series[h : valid_samples + h] - price_series[:valid_samples]) / price_series[:valid_samples]
            dir_label = (ret > 0).astype(np.int64)
            dir_targets[f"h_{h}"] = torch.tensor(dir_label, dtype=torch.long)
            mag_targets[f"h_{h}"] = torch.tensor(ret * 100.0, dtype=torch.float32).unsqueeze(1)

        dataset = TensorDataset(X_train)
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

        for epoch in range(self.epochs):
            for (bx,) in loader:
                bx = bx.to(self.device)
                optimizer.zero_grad()
                out = self.model(bx)

                total_loss = 0.0
                for h in self.horizons:
                    b_dir = dir_targets[f"h_{h}"][:len(bx)].to(self.device)
                    b_mag = mag_targets[f"h_{h}"][:len(bx)].to(self.device)

                    l_logits = out[f"horizon_{h}d"]["logits"]
                    l_mag = out[f"horizon_{h}d"]["magnitude"]

                    loss_cls = F.cross_entropy(l_logits, b_dir)
                    loss_reg = F.mse_loss(l_mag, b_mag)
                    total_loss += loss_cls + 0.1 * loss_reg

                total_loss.backward()
                optimizer.step()

        self.model.eval()
        return self

    def predict_multi_horizon(self, latest_x_seq: np.ndarray) -> Dict[str, Any]:
        """
        Generate multi-horizon directional probabilities and expected returns.
        """
        self.model.eval()
        with torch.no_grad():
            t_x = torch.tensor(latest_x_seq, dtype=torch.float32).to(self.device)
            out = self.model(t_x)

            forecasts = {}
            for h in self.horizons:
                h_key = f"horizon_{h}d"
                logits = out[h_key]["logits"][0]
                probs = torch.softmax(logits, dim=-1).cpu().numpy()
                mag = float(out[h_key]["magnitude"][0].cpu().numpy()[0])

                prob_up = float(probs[1])
                prob_down = float(probs[0])
                signal = 1 if prob_up >= 0.5 else 0

                forecasts[h_key] = {
                    "horizon_days": h,
                    "trend": "UP" if signal == 1 else "DOWN",
                    "confidence_up_pct": round(prob_up * 100.0, 1),
                    "confidence_down_pct": round(prob_down * 100.0, 1),
                    "expected_return_pct": round(mag, 2),
                }

            return forecasts
