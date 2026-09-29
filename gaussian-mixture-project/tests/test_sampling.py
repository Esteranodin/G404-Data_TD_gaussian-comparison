"""Tests pour les fonctions du module sampling."""

import numpy as np
from gaussian.sampling import combine_components, draw_component


def test_draw_component_returns_expected_size_and_type():
    rng = np.random.default_rng(7)
    values = draw_component(rng, mean=100, std_dev=18, size=5)

    assert isinstance(values, np.ndarray)
    assert values.shape == (5,)


def test_draw_component_is_reproducible_with_same_seed():
    values_1 = draw_component(np.random.default_rng(7), 100, 18, 5)
    values_2 = draw_component(np.random.default_rng(7), 100, 18, 5)

    np.testing.assert_array_equal(values_1, values_2)


def test_combine_components_builds_expected_dataframe():
    result = combine_components(np.array([1.0, 2.0]), np.array([3.0]))

    assert list(result.columns) == ["value", "component"]
    assert result["component"].tolist() == ["A", "A", "B"]
    assert result["value"].tolist() == [1.0, 2.0, 3.0]