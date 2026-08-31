"""
StudyChart AI - C Engine Python Bridge.
Provides safe interfaces to C algorithms for statistics, sorting, searching, and regressions.
"""

import ctypes
import os
import math
import statistics
from typing import List, Tuple, Dict, Any, Optional

class DescriptiveStatsStruct(ctypes.Structure):
    _fields_ = [
        ("mean", ctypes.c_double),
        ("variance", ctypes.c_double),
        ("std_dev", ctypes.c_double),
        ("min", ctypes.c_double),
        ("max", ctypes.c_double),
        ("median", ctypes.c_double)
    ]

class LinearRegressionStruct(ctypes.Structure):
    _fields_ = [
        ("slope", ctypes.c_double),
        ("intercept", ctypes.c_double),
        ("r_squared", ctypes.c_double)
    ]

class CEngineBridge:
    _instance = None
    _lib = None

    def __init__(self):
        self._load_library()

    def _load_library(self):
        # Look for precompiled dll/so
        base_dir = os.path.dirname(os.path.abspath(__file__))
        possible_libs = [
            os.path.join(base_dir, "libstudychart_c.so"),
            os.path.join(base_dir, "studychart_c.dll"),
            os.path.join(base_dir, "studychart_c.dylib"),
        ]
        for lib_path in possible_libs:
            if os.path.exists(lib_path):
                try:
                    self._lib = ctypes.CDLL(lib_path)
                    self._setup_function_signatures()
                    break
                except Exception:
                    self._lib = None

    def _setup_function_signatures(self):
        if not self._lib:
            return
        try:
            self._lib.calculate_mean.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
            self._lib.calculate_mean.restype = ctypes.c_double

            self._lib.calculate_descriptive_stats.argtypes = [
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_int,
                ctypes.POINTER(DescriptiveStatsStruct)
            ]
            self._lib.calculate_descriptive_stats.restype = None

            self._lib.calculate_linear_regression.argtypes = [
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_int,
                ctypes.POINTER(LinearRegressionStruct)
            ]
            self._lib.calculate_linear_regression.restype = None

            self._lib.c_binary_search.argtypes = [
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_int,
                ctypes.c_double
            ]
            self._lib.c_binary_search.restype = ctypes.c_int

            self._lib.c_levenshtein_distance.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
            self._lib.c_levenshtein_distance.restype = ctypes.c_int
        except Exception:
            self._lib = None

    def get_descriptive_stats(self, values: List[float]) -> Dict[str, float]:
        if not values:
            return {"mean": 0.0, "variance": 0.0, "std_dev": 0.0, "min": 0.0, "max": 0.0, "median": 0.0}

        if self._lib:
            try:
                arr = (ctypes.c_double * len(values))(*values)
                res = DescriptiveStatsStruct()
                self._lib.calculate_descriptive_stats(arr, len(values), ctypes.byref(res))
                return {
                    "mean": float(res.mean),
                    "variance": float(res.variance),
                    "std_dev": float(res.std_dev),
                    "min": float(res.min),
                    "max": float(res.max),
                    "median": float(res.median),
                }
            except Exception:
                pass

        # High-performance native Python implementation
        n = len(values)
        mean_val = sum(values) / n
        var_val = sum((x - mean_val) ** 2 for x in values) / (n - 1) if n > 1 else 0.0
        std_val = math.sqrt(var_val)
        min_val = min(values)
        max_val = max(values)
        median_val = statistics.median(values)

        return {
            "mean": round(mean_val, 4),
            "variance": round(var_val, 4),
            "std_dev": round(std_val, 4),
            "min": round(min_val, 4),
            "max": round(max_val, 4),
            "median": round(median_val, 4),
        }

    def exponential_moving_average(self, values: List[float], alpha: float = 0.3) -> List[float]:
        if not values:
            return []
        ema = [values[0]]
        for i in range(1, len(values)):
            ema.append(round(alpha * values[i] + (1.0 - alpha) * ema[-1], 4))
        return ema

    def linear_regression(self, x: List[float], y: List[float]) -> Dict[str, float]:
        n = min(len(x), len(y))
        if n <= 1:
            return {"slope": 0.0, "intercept": 0.0, "r_squared": 0.0}

        if self._lib:
            try:
                arr_x = (ctypes.c_double * n)(*x[:n])
                arr_y = (ctypes.c_double * n)(*y[:n])
                res = LinearRegressionStruct()
                self._lib.calculate_linear_regression(arr_x, arr_y, n, ctypes.byref(res))
                return {
                    "slope": float(res.slope),
                    "intercept": float(res.intercept),
                    "r_squared": float(res.r_squared),
                }
            except Exception:
                pass

        x_mean = sum(x[:n]) / n
        y_mean = sum(y[:n]) / n
        num = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        den_x = sum((x[i] - x_mean) ** 2 for i in range(n))
        den_y = sum((y[i] - y_mean) ** 2 for i in range(n))

        slope = num / den_x if den_x != 0 else 0.0
        intercept = y_mean - slope * x_mean
        r_sq = (num / math.sqrt(den_x * den_y)) ** 2 if (den_x * den_y) > 0 else 0.0

        return {
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "r_squared": round(r_sq, 4),
        }

    def binary_search(self, sorted_list: List[float], target: float) -> int:
        if not sorted_list:
            return -1
        left, right = 0, len(sorted_list) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if abs(sorted_list[mid] - target) < 1e-7:
                return mid
            if sorted_list[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def levenshtein_distance(self, s1: str, s2: str) -> int:
        if self._lib:
            try:
                return self._lib.c_levenshtein_distance(s1.encode("utf-8"), s2.encode("utf-8"))
            except Exception:
                pass

        # Native implementation
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
        return dp[m][n]

c_engine = CEngineBridge()

def test_c_engine():
    data = [10.0, 20.0, 30.0, 40.0, 50.0]
    stats = c_engine.get_descriptive_stats(data)
    assert stats["mean"] == 30.0, f"Expected 30.0, got {stats['mean']}"
    assert stats["median"] == 30.0
    print("[OK] C Engine tests passed successfully.")

if __name__ == "__main__":
    test_c_engine()
