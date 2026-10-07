"""
Stock Market Trend Prediction Platform
Based on Comparative Analysis of Machine Learning and Deep Learning Algorithms
via Continuous and Binary Data.
"""

import os
import sys

# Ensure torch DLL directory is registered on Windows to prevent WinError 1114
_DLL_HANDLES = []
if sys.platform == "win32":
    for _p in sys.path:
        _cand = os.path.join(_p, "torch", "lib")
        if os.path.isdir(_cand):
            try:
                _DLL_HANDLES.append(os.add_dll_directory(_cand))
                os.environ["PATH"] = _cand + os.pathsep + os.environ.get("PATH", "")
            except Exception:
                pass
            break
    try:
        import torch  # Initialize PyTorch while DLL handle is actively registered
    except Exception:
        pass

__version__ = "1.0.0"


