"""Show three views of the same sample from one normal distribution."""

import numpy as np
import plotly.express as px

mean = 0
std_dev = 1
size = 1000
seed = 404
rng = np.random.default_rng(seed)
values = rng.normal(loc=mean, scale=std_dev, size=size)

histogram_figure = px.histogram(
    x=values,
    nbins=30,
    histnorm="probability density",
    title="Distribution simulée",
    labels={"x": "Valeur"},
)
histogram_figure.update_yaxes(title_text="Densité")
histogram_figure.show()

box_figure = px.box(
    x=values,
    points=False,
    title="Médiane et dispersion",
    labels={"x": "Valeur"},
)
box_figure.show()

cumulative_figure = px.ecdf(
    x=values,
    ecdfnorm="probability",
    title="Répartition cumulée des valeurs",
    labels={"x": "Valeur"},
)
cumulative_figure.update_yaxes(title_text="Proportion cumulée")
cumulative_figure.show()
