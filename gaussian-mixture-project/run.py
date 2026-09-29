"""Script de lancement : crée deux mélanges gaussiens et affiche leurs résultats."""

from gaussian import DEFAULT_SEED
from gaussian.mixture import GaussianMixture

N_OBSERVATIONS = 2000
SEED = DEFAULT_SEED

# Paramètres du premier objet
MEAN_A = 100
STD_A = 18
MEAN_B = 106
STD_B = 24
WEIGHT_A = 0.6

# Paramètres du second objet
SECOND_WEIGHT_A = 0.3
SECOND_STD_B = 30


def main():
    first = GaussianMixture(MEAN_A, STD_A, MEAN_B, STD_B, weight_a=WEIGHT_A)
    first_sample = first.sample(N_OBSERVATIONS, seed=SEED)

    print("Premier objet")
    print(first_sample["component"].value_counts())
    print()

    first.plot_components().show()
    first.plot_mixture().show()
    first.plot_box().show()

    second = GaussianMixture(MEAN_A, STD_A, MEAN_B, SECOND_STD_B, weight_a=SECOND_WEIGHT_A)
    second_sample = second.sample(N_OBSERVATIONS, seed=SEED)

    print("Second objet")
    print(second_sample["component"].value_counts())


if __name__ == "__main__":
    main()