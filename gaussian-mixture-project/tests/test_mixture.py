"""Tests pour la classe GaussianMixture."""

import pytest
from gaussian.mixture import GaussianMixture


def test_sample_returns_expected_shape_and_counts():
    model = GaussianMixture(mean_a=100, std_a=18, mean_b=106, std_b=24, weight_a=0.6)
    sample = model.sample(n=2000, seed=404)

    assert sample is model.samples
    assert sample.shape == (2000, 2)
    assert sample["component"].value_counts().to_dict() == {"A": 1200, "B": 800}


def test_sample_is_reproducible_with_same_seed():
    model_1 = GaussianMixture(100, 18, 106, 24, weight_a=0.6)
    model_2 = GaussianMixture(100, 18, 106, 24, weight_a=0.6)

    sample_1 = model_1.sample(n=2000, seed=404)
    sample_2 = model_2.sample(n=2000, seed=404)

    assert sample_1["value"].tolist() == sample_2["value"].tolist()
    assert sample_1["component"].tolist() == sample_2["component"].tolist()


def test_two_instances_are_independent():
    first = GaussianMixture(100, 18, 106, 24, weight_a=0.6)
    first_samples = first.sample(n=2000, seed=404)

    second = GaussianMixture(100, 18, 106, 30, weight_a=0.3)
    second_samples = second.sample(n=2000, seed=404)

    assert first_samples is not second_samples
    assert first_samples["component"].value_counts().to_dict() == {"A": 1200, "B": 800}
    assert second_samples["component"].value_counts().to_dict() == {"A": 600, "B": 1400}


def test_sample_rejects_non_integer_n():
    model = GaussianMixture(100, 18, 106, 24, weight_a=0.6)

    with pytest.raises(TypeError):
        model.sample(n=2000.0, seed=404)


def test_sample_rejects_n_lower_two():
    model = GaussianMixture(100, 18, 106, 24, weight_a=0.6)

    with pytest.raises(ValueError):
        model.sample(n=1, seed=404)


def test_sample_rejects_non_positive_std():
    model = GaussianMixture(100, std_a=0, mean_b=106, std_b=24, weight_a=0.6)

    with pytest.raises(ValueError):
        model.sample(n=2000, seed=404)


def test_sample_rejects_weight_outside_open_interval():
    model = GaussianMixture(100, 18, 106, 24, weight_a=1.0)

    with pytest.raises(ValueError):
        model.sample(n=2000, seed=404)


def test_sample_rejects_empty_group_from_rounding():
    model = GaussianMixture(100, 18, 106, 24, weight_a=0.1)

    with pytest.raises(ValueError):
        model.sample(n=2, seed=404)