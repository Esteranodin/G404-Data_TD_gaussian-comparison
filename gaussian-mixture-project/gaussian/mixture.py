"""Classe représentant un mélange de deux distributions gaussiennes."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# imports relatifs qui désignent module du même paquet
from . import DEFAULT_SEED
from .sampling import combine_components, draw_component


class GaussianMixture:
    """Deux composantes gaussiennes, un échantillon reproductible et ses vues."""

    def __init__(self, mean_a, std_a, mean_b, std_b, weight_a=0.6):
        self.mean_a = mean_a
        self.std_a = std_a
        self.mean_b = mean_b
        self.std_b = std_b
        self.weight_a = weight_a
        self.samples: pd.DataFrame | None = None

    def sample(self, n, seed=DEFAULT_SEED) -> pd.DataFrame:
        """Tire n observations et les garde sur l'instance."""
        if not isinstance(n, int):
            raise TypeError("n doit être un entier")
        if n < 2:
            raise ValueError("n doit être au moins égal à 2")
        if self.std_a <= 0 or self.std_b <= 0:
            raise ValueError("Les écarts-types doivent être strictement positifs")
        if not (0 < self.weight_a < 1):
            raise ValueError("weight_a doit être strictement compris entre 0 et 1")

        n_a = int(n * self.weight_a)
        n_b = n - n_a

        if n_a < 1 or n_b < 1:
            raise ValueError("Chaque groupe doit contenir au moins une observation")

        generator = np.random.default_rng(seed)
        values_a = draw_component(generator, self.mean_a, self.std_a, n_a)
        values_b = draw_component(generator, self.mean_b, self.std_b, n_b)

        self.samples = combine_components(values_a, values_b)
        return self.samples

    # _devant méthode suivante = méthode privée 
    def _check_samples(self) -> pd.DataFrame:
        """Vérifie qu'un échantillon existe avant de tracer une figure."""
        if self.samples is None:
            raise RuntimeError("Appelez sample() avant de tracer une figure")
        return self.samples

    def plot_components(self) -> go.Figure:
        """Superpose les histogrammes de A et B pour les comparer."""
        samples =self._check_samples()
        return px.histogram(
            samples,
            x="value",
            color="component",
            histnorm="probability density",
            barmode="overlay",
            nbins=45,
            opacity=0.65,
            title="Comparaison des composantes A et B",
            labels={"value": "Valeur", "component": "Composante"},
        )

    def plot_mixture(self) -> go.Figure:
        """Trace un histogramme du mélange, sans distinguer les groupes."""
        samples =self._check_samples()
        return px.histogram(
            samples,
            x="value",
            histnorm="probability density",
            title="Mélange A + B (sans distinction)",
            labels={"value": "Valeur"},
        )

    def plot_box(self) -> go.Figure:
        """Compare A, B et leur mélange (A∪B) avec des boîtes à moustaches."""
        samples =self._check_samples()
        mixture_rows = samples.copy()
        mixture_rows["component"] = "A∪B"

        combined_for_plot = pd.concat([self.samples, mixture_rows], ignore_index=True)

        return px.box(
            combined_for_plot,
            x="component",
            y="value",
            title="Médianes et dispersion : A, B et le mélange",
            labels={"value": "Valeur", "component": "Groupe"},
        )