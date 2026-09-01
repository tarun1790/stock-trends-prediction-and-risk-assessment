"""
Deep Learning and Neural Network Models (GPU/CUDA Accelerated).
Implements PyTorch implementations of:
- ANN (Artificial Neural Network / MLP)
- RNN (Recurrent Neural Network with sequence window 1-30 days)
- LSTM (Long Short-Term Memory Network)
- GRU (Gated Recurrent Unit)
- BiLSTM with Temporal Self-Attention
- Time-Series Transformer Classifier
Configured for GPU/CUDA acceleration by default.
"""

import math
import copy
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from stock_predict.config import get_device
from stock_predict.models.base import BaseModelWrapper


def get_activation(name: str) -> nn.Module:
    """Map activation function name to PyTorch activation module."""
    name_lower = name.lower()
    if name_lower == "relu":
        return nn.ReLU()
    elif name_lower == "tanh":
        return nn.Tanh()
    elif name_lower == "sigmoid":
        return nn.Sigmoid()
    elif name_lower == "leaky_relu" or name_lower == "leakyrelu":
        return nn.LeakyReLU(negative_slope=0.01)
    elif name_lower == "gelu":
        return nn.GELU()
    return nn.ReLU()


# -------------------------------------------------------------------------
# PyTorch Module Definitions
# -------------------------------------------------------------------------

class PyTorchANN(nn.Module):
    """
    Artificial Neural Network (MLP) architecture.
    Matches Table 3 & Figures 11-12 of the IEEE paper.
    """

    def __init__(
        self,
        input_dim: int = 10,
        hidden_dims: List[int] = None,
        activation: str = "relu",
        dropout: float = 0.2,
        num_classes: int = 2,
    ):
        super().__init__()
        if hidden_dims is None:
            hidden_dims = [200, 100]

        layers: List[nn.Module] = []
        prev_dim = input_dim
        act_mod = get_activation(activation)

        for h_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(nn.BatchNorm1d(h_dim))
            layers.append(copy.deepcopy(act_mod))
            if dropout > 0.0:
                layers.append(nn.Dropout(dropout))
            prev_dim = h_dim

        layers.append(nn.Linear(prev_dim, num_classes))
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 3:
            # Flatten or take last timestep if 3D tensor is passed
            x = x[:, -1, :]
        return self.network(x)


class PyTorchRNN(nn.Module):
    """
    Recurrent Neural Network (Elman RNN).
    Matches Table 3 & Figure 13 of the IEEE paper.
    """

    def __init__(
        self,
        input_dim: int = 10,
        hidden_dim: int = 500,
        num_layers: int = 2,
        nonlinearity: str = "tanh",
        dropout: float = 0.2,
        num_classes: int = 2,
    ):
        super().__init__()
        self.rnn = nn.RNN(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            nonlinearity="tanh" if nonlinearity == "tanh" else "relu",
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 2:
            x = x.unsqueeze(1)  # (batch, 1, features)
        out, _ = self.rnn(x)
        last_step = out[:, -1, :]
        out = self.dropout(last_step)
        return self.fc(out)


class PyTorchLSTM(nn.Module):
    """
    Long Short-Term Memory (LSTM) Network.
    Matches Section III-K and Table 3 of the IEEE paper.
    """

    def __init__(
        self,
        input_dim: int = 10,
        hidden_dim: int = 500,
        num_layers: int = 2,
        dropout: float = 0.2,
        bidirectional: bool = False,
        num_classes: int = 2,
    ):
        super().__init__()
        self.bidirectional = bidirectional
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
            bidirectional=bidirectional,
        )
        fc_in = hidden_dim * 2 if bidirectional else hidden_dim
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(fc_in, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 2:
            x = x.unsqueeze(1)
        out, _ = self.lstm(x)
        last_step = out[:, -1, :]
        out = self.dropout(last_step)
        return self.fc(out)


class PyTorchGRU(nn.Module):
    """
    Gated Recurrent Unit (GRU) Network.
    Advanced high-efficiency time series architecture.
    """

    def __init__(
        self,
        input_dim: int = 10,
        hidden_dim: int = 256,
        num_layers: int = 2,
        dropout: float = 0.2,
        num_classes: int = 2,
    ):
        super().__init__()
        self.gru = nn.GRU(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 2:
            x = x.unsqueeze(1)
        out, _ = self.gru(x)
        last_step = out[:, -1, :]
        out = self.dropout(last_step)
        return self.fc(out)


class AttentionBlock(nn.Module):
    """Temporal Multi-Head Attention layer over time-series steps."""

    def __init__(self, hidden_dim: int, num_heads: int = 4):
        super().__init__()
        self.mha = nn.MultiheadAttention(
            embed_dim=hidden_dim, num_heads=num_heads, batch_first=True
        )
        self.norm = nn.LayerNorm(hidden_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, seq_len, hidden_dim)
        attn_out, _ = self.mha(x, x, x)
        x = self.norm(x + attn_out)
        return x


class PyTorchBiLSTMAttention(nn.Module):
    """
    Bidirectional LSTM with Temporal Self-Attention Mechanism.
    """

    def __init__(
        self,
        input_dim: int = 10,
        hidden_dim: int = 256,
        num_layers: int = 2,
        num_heads: int = 4,
        dropout: float = 0.2,
        num_classes: int = 2,
    ):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim // 2,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.attention = AttentionBlock(hidden_dim, num_heads=num_heads)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 2:
            x = x.unsqueeze(1)
        lstm_out, _ = self.lstm(x)
        attn_out = self.attention(lstm_out)
        pooled = torch.mean(attn_out, dim=1)  # Temporal global average pooling
        pooled = self.dropout(pooled)
        return self.fc(pooled)


class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 100):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, seq_len, d_model)
        seq_len = x.size(1)
        return x + self.pe[:, :seq_len, :]


class PyTorchTransformer(nn.Module):
    """
    Time-Series Transformer Classifier.
    """

    def __init__(
        self,
        input_dim: int = 10,
        d_model: int = 64,
        nhead: int = 4,
        num_layers: int = 2,
        dim_feedforward: int = 128,
        dropout: float = 0.2,
        num_classes: int = 2,
    ):
        super().__init__()
        self.input_projection = nn.Linear(input_dim, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
            activation="gelu",
        )
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer, num_layers=num_layers
        )
        self.fc = nn.Sequential(
            nn.Linear(d_model, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 2:
            x = x.unsqueeze(1)
        x = self.input_projection(x)
        x = self.pos_encoder(x)
        x = self.transformer_encoder(x)
        pooled = torch.mean(x, dim=1)
        return self.fc(pooled)


# -------------------------------------------------------------------------
# PyTorch Model Wrapper with Scikit-Learn Style Interface & GPU Execution
# -------------------------------------------------------------------------

class PyTorchModelWrapper(BaseModelWrapper):
    """
    Unified PyTorch wrapper managing GPU allocation, training loops,
    early stopping, mini-batching, and scikit-learn compatible inference.
    """

    def __init__(
        self,
        model_type: str,
        name: str,
        input_dim: int = 10,
        hidden_dim: int = 500,
        learning_rate: float = 0.001,
        weight_decay: float = 1e-5,
        batch_size: int = 64,
        epochs: int = 100,
        patience: int = 20,
        device: Optional[torch.device] = None,
        **kwargs,
    ):
        params = {
            "model_type": model_type,
            "input_dim": input_dim,
            "hidden_dim": hidden_dim,
            "learning_rate": learning_rate,
            "weight_decay": weight_decay,
            "batch_size": batch_size,
            "epochs": epochs,
            "patience": patience,
            **kwargs,
        }
        super().__init__(name, params)
        self.model_type = model_type
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.batch_size = batch_size
        self.epochs = epochs
        self.patience = patience
        self.kwargs = kwargs

        # Always default to GPU/CUDA if available
        self.device = device or get_device()
        self.torch_model = self._build_model().to(self.device)
        self.criterion = nn.CrossEntropyLoss()

    def _build_model(self) -> nn.Module:
        mtype = self.model_type.lower()
        if mtype == "ann":
            hidden_dims = self.kwargs.get("hidden_dims", [self.hidden_dim, self.hidden_dim // 2])
            activation = self.kwargs.get("activation", "relu")
            return PyTorchANN(
                input_dim=self.input_dim,
                hidden_dims=hidden_dims,
                activation=activation,
                dropout=self.kwargs.get("dropout", 0.2),
            )
        elif mtype == "rnn":
            return PyTorchRNN(
                input_dim=self.input_dim,
                hidden_dim=self.hidden_dim,
                num_layers=self.kwargs.get("num_layers", 2),
                nonlinearity=self.kwargs.get("nonlinearity", "tanh"),
                dropout=self.kwargs.get("dropout", 0.2),
            )
        elif mtype == "lstm":
            return PyTorchLSTM(
                input_dim=self.input_dim,
                hidden_dim=self.hidden_dim,
                num_layers=self.kwargs.get("num_layers", 2),
                dropout=self.kwargs.get("dropout", 0.2),
                bidirectional=self.kwargs.get("bidirectional", False),
            )
        elif mtype == "gru":
            return PyTorchGRU(
                input_dim=self.input_dim,
                hidden_dim=self.hidden_dim,
                num_layers=self.kwargs.get("num_layers", 2),
                dropout=self.kwargs.get("dropout", 0.2),
            )
        elif mtype == "bilstm_attention":
            return PyTorchBiLSTMAttention(
                input_dim=self.input_dim,
                hidden_dim=self.hidden_dim,
                num_layers=self.kwargs.get("num_layers", 2),
                num_heads=self.kwargs.get("num_heads", 4),
                dropout=self.kwargs.get("dropout", 0.2),
            )
        elif mtype == "transformer":
            return PyTorchTransformer(
                input_dim=self.input_dim,
                d_model=self.kwargs.get("d_model", 64),
                nhead=self.kwargs.get("nhead", 4),
                num_layers=self.kwargs.get("num_layers", 2),
                dropout=self.kwargs.get("dropout", 0.2),
            )
        elif mtype == "tcn":
            from stock_predict.models.advanced_neural import PyTorchTCN
            return PyTorchTCN(
                input_dim=self.input_dim,
                dropout=self.kwargs.get("dropout", 0.2),
            )
        elif mtype == "tft":
            from stock_predict.models.advanced_neural import PyTorchTFT
            return PyTorchTFT(
                input_dim=self.input_dim,
                hidden_dim=self.kwargs.get("hidden_dim", 64),
                dropout=self.kwargs.get("dropout", 0.1),
            )
        else:
            raise ValueError(f"Unknown neural model type: '{self.model_type}'")

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        verbose: bool = False,
    ) -> "PyTorchModelWrapper":
        """
        Train neural model with mini-batch Adam optimization and Early Stopping.
        """
        self.torch_model = self.torch_model.to(self.device)
        optimizer = optim.Adam(
            self.torch_model.parameters(),
            lr=self.learning_rate,
            betas=(0.9, 0.999),
            weight_decay=self.weight_decay,
        )

        train_dataset = TensorDataset(
            torch.tensor(X_train, dtype=torch.float32),
            torch.tensor(y_train, dtype=torch.long),
        )
        train_loader = DataLoader(
            train_dataset, batch_size=self.batch_size, shuffle=True
        )

        val_loader = None
        if X_val is not None and y_val is not None:
            val_dataset = TensorDataset(
                torch.tensor(X_val, dtype=torch.float32),
                torch.tensor(y_val, dtype=torch.long),
            )
            val_loader = DataLoader(
                val_dataset, batch_size=self.batch_size, shuffle=False
            )

        best_val_loss = float("inf")
        best_state = None
        patience_counter = 0

        self.torch_model.train()
        for epoch in range(self.epochs):
            running_loss = 0.0
            for batch_x, batch_y in train_loader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device)

                optimizer.zero_grad()
                outputs = self.torch_model(batch_x)
                if isinstance(outputs, tuple):
                    outputs = outputs[0]
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                running_loss += loss.item() * batch_x.size(0)

            epoch_train_loss = running_loss / len(train_dataset)

            # Validation & Early Stopping
            if val_loader is not None:
                self.torch_model.eval()
                val_loss = 0.0
                with torch.no_grad():
                    for val_x, val_y in val_loader:
                        val_x = val_x.to(self.device)
                        val_y = val_y.to(self.device)
                        val_outputs = self.torch_model(val_x)
                        if isinstance(val_outputs, tuple):
                            val_outputs = val_outputs[0]
                        v_loss = self.criterion(val_outputs, val_y)
                        val_loss += v_loss.item() * val_x.size(0)

                epoch_val_loss = val_loss / len(val_dataset)
                self.torch_model.train()

                if epoch_val_loss < best_val_loss:
                    best_val_loss = epoch_val_loss
                    best_state = copy.deepcopy(self.torch_model.state_dict())
                    patience_counter = 0
                else:
                    patience_counter += 1
                    if patience_counter >= self.patience:
                        if verbose:
                            print(f"Early stopping triggered at epoch {epoch+1}")
                        break

        if best_state is not None:
            self.torch_model.load_state_dict(best_state)

        self.torch_model.eval()
        self.is_fitted = True
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        self.torch_model.eval()
        with torch.no_grad():
            tensor_x = torch.tensor(X, dtype=torch.float32).to(self.device)
            logits = self.torch_model(tensor_x)
            if isinstance(logits, tuple):
                logits = logits[0]
            probs = torch.softmax(logits, dim=-1)
            return probs.cpu().numpy()

    def predict(self, X: np.ndarray) -> np.ndarray:
        probs = self.predict_proba(X)
        return np.argmax(probs, axis=1)


# Factory constructors for direct instantiation
def create_ann_model(
    input_dim: int = 10,
    hidden_dims: List[int] = None,
    activation: str = "relu",
    lr: float = 0.001,
    epochs: int = 150,
) -> PyTorchModelWrapper:
    return PyTorchModelWrapper(
        model_type="ann",
        name="ANN",
        input_dim=input_dim,
        hidden_dims=hidden_dims or [500, 200],
        activation=activation,
        learning_rate=lr,
        epochs=epochs,
    )


def create_rnn_model(
    input_dim: int = 10,
    hidden_dim: int = 500,
    lr: float = 0.00005,
    epochs: int = 100,
) -> PyTorchModelWrapper:
    return PyTorchModelWrapper(
        model_type="rnn",
        name="RNN",
        input_dim=input_dim,
        hidden_dim=hidden_dim,
        learning_rate=lr,
        epochs=epochs,
    )


def create_lstm_model(
    input_dim: int = 10,
    hidden_dim: int = 500,
    lr: float = 0.00005,
    epochs: int = 100,
) -> PyTorchModelWrapper:
    return PyTorchModelWrapper(
        model_type="lstm",
        name="LSTM",
        input_dim=input_dim,
        hidden_dim=hidden_dim,
        learning_rate=lr,
        epochs=epochs,
    )


def create_gru_model(
    input_dim: int = 10,
    hidden_dim: int = 256,
    lr: float = 0.0001,
    epochs: int = 100,
) -> PyTorchModelWrapper:
    return PyTorchModelWrapper(
        model_type="gru",
        name="GRU",
        input_dim=input_dim,
        hidden_dim=hidden_dim,
        learning_rate=lr,
        epochs=epochs,
    )


def create_bilstm_attention_model(
    input_dim: int = 10,
    hidden_dim: int = 256,
    lr: float = 0.0001,
    epochs: int = 100,
) -> PyTorchModelWrapper:
    return PyTorchModelWrapper(
        model_type="bilstm_attention",
        name="BiLSTM-Attention",
        input_dim=input_dim,
        hidden_dim=hidden_dim,
        learning_rate=lr,
        epochs=epochs,
    )


def create_transformer_model(
    input_dim: int = 10,
    d_model: int = 64,
    lr: float = 0.0002,
    epochs: int = 100,
) -> PyTorchModelWrapper:
    return PyTorchModelWrapper(
        model_type="transformer",
        name="Transformer",
        input_dim=input_dim,
        d_model=d_model,
        learning_rate=lr,
        epochs=epochs,
    )
