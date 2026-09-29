"""Descriptive and inferential tools for comparing two groups."""

from .descriptive import describe_groups, mean_comparison
from .inference import welch_mean_test
from .sampling_variation import simulate_mean_differences

__all__ = [
    "describe_groups",
    "mean_comparison",
    "simulate_mean_differences",
    "welch_mean_test",
]
