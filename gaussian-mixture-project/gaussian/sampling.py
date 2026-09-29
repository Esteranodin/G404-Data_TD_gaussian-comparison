"""Fonctions de tirage et d'assemblage pour le mélange gaussien."""

import numpy as np
import pandas as pd


def draw_component(rng, mean, std_dev, size) -> np.ndarray:
    """Draw size values from one Gaussian distribution."""
    return rng.normal(loc=mean, scale=std_dev, size=size)


def combine_components(values_a, values_b) -> pd.DataFrame:
    """Return a long table with value and component columns."""
    return pd.DataFrame({
        "value": np.concatenate([values_a, values_b]),
        "component": ["A"] * len(values_a) + ["B"] * len(values_b),
    })