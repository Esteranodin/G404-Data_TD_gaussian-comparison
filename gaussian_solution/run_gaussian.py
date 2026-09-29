"""Run one simulation and display its visual dashboard."""

from distributions import DEFAULT_SEED
from distributions.gaussian_mixture import GaussianMixture
from distributions.gaussian_plots import (
    plot_box,
    plot_components,
    plot_dashboard,
    plot_ecdf,
    plot_mixture,
    plot_violin,
)


def main():
    """Create one model, print its summary and show one dashboard."""
    mean_a = 100
    std_a = 18
    mean_b = 106
    std_b = 24
    weight_a = 0.6
    n = 2000
    seed = DEFAULT_SEED

    model = GaussianMixture(mean_a, std_a, mean_b, std_b, weight_a)
    samples = model.sample(n, seed)

    print("Sample summary:")
    print(samples.groupby("component")["value"].agg(["count", "mean", "std"]))

    print("\nStandalone plot options:")
    for plot_function in (
        plot_components,
        plot_mixture,
        plot_box,
        plot_ecdf,
        plot_violin,
    ):
        print(f"- {plot_function.__name__}(model).show()")

    # One browser view combines the four complementary readings.
    plot_dashboard(model).show()


if __name__ == "__main__":
    main()
