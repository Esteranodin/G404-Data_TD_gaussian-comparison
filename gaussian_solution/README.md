# Deux groupes gaussiens — projet de référence et comparaison

Un lanceur, un paquet local et des tests qui importent la même classe.  
Le paquet `analysis` ajoute ensuite `descriptive.py` et `inference.py` pour décrire A et B et comparer leurs moyennes.

## Organisation

```text
gaussian_project_solution/
├── run_gaussian.py
├── run_sampling_variation.py
├── compare_processes.py
├── distributions/
│   ├── __init__.py
│   ├── gaussian_mixture.py
│   └── gaussian_plots.py
├── analysis/
│   ├── __init__.py
│   ├── descriptive.py
│   ├── inference.py
│   ├── inference_plots.py
│   └── sampling_variation.py
├── tests/
│   ├── test_gaussian_mixture.py
│   └── test_analysis.py
├── requirements.txt
└── README.md
```

| Projet Rectangle | Projet gaussien | Rôle |
| --- | --- | --- |
| `run_rectangle.py` | [run_gaussian.py](run_gaussian.py) | Choisir les paramètres, créer le modèle et afficher les résultats |
| `geometry/__init__.py` | [distributions/__init__.py](distributions/__init__.py) | Définir une constante partagée : ici `DEFAULT_SEED` |
| `geometry/rectangle.py` | [distributions/gaussian_mixture.py](distributions/gaussian_mixture.py) | Définir la classe, tirer les valeurs et assembler le dataframe |
| — | [distributions/gaussian_plots.py](distributions/gaussian_plots.py) | Construire les figures à partir d'un objet déjà échantillonné |
| — | [analysis/sampling_variation.py](analysis/sampling_variation.py) | Répéter les tirages sous H₀ et conserver `avg(B) − avg(A)` |
| — | [analysis/inference_plots.py](analysis/inference_plots.py) | Construire l'histogramme Plotly des différences simulées |
| — | [run_sampling_variation.py](run_sampling_variation.py) | Reproduire la figure de la diapositive 30 |
| `tests/test_rectangle.py` | [tests/test_gaussian_mixture.py](tests/test_gaussian_mixture.py) | Vérifier la classe utilisée par le lanceur |
| — | [analysis/descriptive.py](analysis/descriptive.py) | Décrire A et B et mesurer leur écart observé |
| — | [analysis/inference.py](analysis/inference.py) | Estimer et tester la différence de moyennes |
| — | [compare_processes.py](compare_processes.py) | Lancer la comparaison descriptive et formelle |
| — | [tests/test_analysis.py](tests/test_analysis.py) | Vérifier les nouveaux calculs |

Le lanceur et les tests utilisent le même import :

```python
from distributions.gaussian_mixture import GaussianMixture
from distributions.gaussian_plots import plot_components, plot_dashboard
```

Dans le paquet, `from . import DEFAULT_SEED` lit la constante de `__init__.py`.
L'import des modules définit le code sans lancer de simulation ni afficher de
figure. `gaussian_mixture.py` conserve les paramètres et produit les valeurs ;
`gaussian_plots.py` lit l'objet échantillonné et construit les figures. Leurs
contrôles rapides ne démarrent que si le module concerné est choisi comme point
d'entrée. La simulation sous H₀ et sa figure Plotly suivent la même
séparation : un module calcule les différences, un autre construit la figure et
le lanceur choisit de l'afficher ou de l'exporter.

## Exécuter

Depuis **ce dossier**, avec le Python du cours :

```bash
python -m pip install -r requirements.txt
python run_gaussian.py
python run_sampling_variation.py
python -m unittest discover -s tests -v
python compare_processes.py
```

Lancez les tests depuis la racine du projet.
Le paquet local est alors accessible sans réglage de `PYTHONPATH`.
Aucun autre dossier du cours n'est nécessaire.

`run_sampling_variation.py` affiche la distribution Plotly interactive utilisée
sur la diapositive 30. L'export PNG est facultatif :

```bash
python run_sampling_variation.py --output sampling_variation.png --no-show
```

L'export statique utilise Kaleido et un navigateur Chrome ou Chromium installé.
L'affichage interactif ordinaire ne dépend pas de cette option.

## Exécuter avec Quick Run dans l'espace de travail g404

- `run_gaussian.py` décrit l'échantillon et affiche un tableau de bord en une
  seule fenêtre ;
- `run_sampling_variation.py` répète les tirages sous H₀ et affiche la figure
  Plotly de la diapositive 30 sans écrire de fichier ;
- `compare_processes.py` affiche la comparaison statistique ;
- `distributions/gaussian_mixture.py` vérifie le tirage reproductible, les
  effectifs et les métadonnées conservées ;
- `distributions/gaussian_plots.py` construit les six figures, vérifie leur
  structure et affiche uniquement le tableau de bord ;
- `tests/test_gaussian_mixture.py` lance ses dix tests du projet initial et de
  ses vues graphiques ;
- `tests/test_analysis.py` lance ses sept tests de l'extension statistique.

Quick Run reconnaît les deux fichiers comme des modules du paquet et utilise
`python -m distributions.gaussian_mixture` ou
`python -m distributions.gaussian_plots`. Les autres fichiers de
`distributions/` et `analysis/` restent des modules importés : vérifiez-les avec
le fichier de tests correspondant plutôt qu'en les lançant seuls.

Cette option dépend de la tâche configurée dans l'espace de travail g404 : elle
ajoute la racine du projet au chemin des imports. Pour un fichier placé dans
`tests/`, le lanceur ajoute aussi automatiquement le dossier parent de `tests/` ;
les imports locaux restent donc disponibles même si le terminal n'a pas encore
rechargé son `PYTHONPATH`. Quick Run démarre ensuite le point d'entrée
sélectionné. Lorsqu'un bloc `if __name__ == "__main__"` est présent, il lance le
contrôle prévu.
Pour une copie extraite ailleurs, utilisez les commandes du terminal ci-dessus.
Les contrôles rapides facultatifs se lancent depuis la racine du projet avec
`python -m distributions.gaussian_mixture` et
`python -m distributions.gaussian_plots` ; `unittest discover` lance les
dix-sept tests et reste la vérification complète.

## Suivre les données

`run_gaussian.py` choisit les paramètres et crée un modèle. La méthode
`sample()` tire A puis B avec un même générateur, appelle la méthode privée
`_combine_components()` pour construire le dataframe, le conserve dans
`self.samples` et renvoie ce même objet. Les fonctions de `gaussian_plots.py`
reçoivent l'objet, lisent ce dataframe et renvoient les figures ; le lanceur
choisit ce qu'il affiche.

Avant `sample()`, `model.samples` peut légitimement valoir `None`. L'annotation
`pd.DataFrame | None` décrit ces deux états possibles. En revanche, la signature
`sample() -> pd.DataFrame` garantit le type de la valeur renvoyée par cet appel :
le lanceur la nomme `samples`, et Pylance peut alors proposer directement les
méthodes comme `groupby()`. Après l'appel, `samples` et `model.samples` désignent
le même dataframe. Ces annotations aident l'éditeur mais ne contrôlent pas
l'exécution ; `_require_samples()` reste la vérification au moment de construire
une figure.

- Échantillon : **1 200 A et 800 B** ; moyennes théoriques 100/106,
  écarts-types 18/24, 60 % de A, 2 000 observations, `seed=404`.
- Le terminal décrit cet échantillon et donne les appels des cinq vues
  autonomes. Une seule fenêtre affiche le **tableau de bord du modèle** :
  A/B séparés, mélange, violons et proportions cumulées. Les données
  conservées dans l'objet restent inchangées.
- Un test séparé crée deux instances et vérifie qu'elles ne partagent ni leur
  configuration, ni leur dataframe mutable.

Les mêmes paramètres et la même seed reproduisent les valeurs dans le même
environnement. Cette version utilise les paramètres valides du cours ; le tirage
précède les graphiques.

## Lire les figures sans les confondre

- `plot_components()` superpose deux **histogrammes observés, normalisés en
  densité**. A et B utilisent exactement les mêmes intervalles d'histogramme.
  Les courbes sont les lois normales théoriques calculées avec `mean_a`,
  `std_a`, `mean_b` et `std_b` ; elles ne sont pas ajustées aux observations.
- `plot_mixture()` réunit toutes les observations dans un histogramme. Les
  courbes A et B sont les **contributions théoriques pondérées** par `weight_a`
  et `1 - weight_a`. Leur somme point par point donne la densité théorique du
  mélange. Une contribution pondérée n'est pas une densité normalisée à 1.
- `plot_box()` est une option autonome qui compare centre, dispersion et valeurs
  atypiques pour A, B et A∪B. `plot_ecdf()` trace la fonction de répartition
  empirique (ECDF) : pour chaque valeur x, elle donne la proportion
  d'observations inférieures ou égales à x.
- `plot_violin()` montre une estimation lissée de la densité locale ; sa largeur
  ne représente pas l'effectif du groupe. La boîte et la ligne moyenne à
  l'intérieur aident à garder des repères.
- `plot_dashboard()` réunit les quatre lectures complémentaires les plus utiles
  dans une même fenêtre. Les couleurs de A et B et les styles de lignes restent
  identiques d'un panneau à l'autre.

Le poids théorique vient de la configuration du modèle. Pour de très petits
échantillons, `int(n * weight_a)` arrondit l'effectif de A : la proportion
observée peut alors différer légèrement du poids du modèle. Avec 2 000
observations et `weight_a=0.6`, les deux valent exactement 60 %.

## Comparer A et B

`analysis/descriptive.py` commence par les observations : effectif, moyenne,
médiane, écart-type, quartiles et intervalle interquartile de chaque groupe.
`mean_comparison()` calcule la différence **avg(B) − avg(A)**, où `avg(G)`
désigne la moyenne observée du groupe G, ainsi qu'une différence standardisée.
Une valeur positive indique
donc que la moyenne observée de B est supérieure à celle de A.

`analysis/inference.py` applique le test de Welch à deux groupes indépendants.
Ce test n'impose pas des variances égales. Il renvoie la différence observée,
un intervalle de confiance, la statistique de test, les degrés de liberté et la
valeur p. L'intervalle et la valeur p quantifient l'incertitude statistique ;
ils ne décident pas si l'écart est important dans le contexte étudié.

Avec la graine 404, la différence observée avg(B) − avg(A) vaut environ 5.862.
L'intervalle de confiance de μ₂ − μ₁ va approximativement de 3.877 à 7.846 et la
différence standardisée vaut environ 0.281. Le grand nombre d'observations rend
l'écart statistiquement net, mais son importance pratique reste à interpréter.

`run_sampling_variation.py` construit ensuite un modèle nul dont les deux
moyennes valent 103, tout en conservant les écarts-types 18 et 24, l'effectif
total 2 000 et la répartition 60 % / 40 %. Il appelle
`GaussianMixture.sample()` avec 5 000 seeds distinctes et conserve une valeur
`avg(B) − avg(A)` par répétition. La figure obtenue est une distribution de
différences de moyennes sous H₀, pas la distribution de la statistique T de
Welch et pas une valeur p simulée.

## Limites de l'exemple

Le dataframe contient **une variable numérique**, `value`, et le libellé de
groupe `component`. Deux groupes ne sont pas deux variables mesurées. La
simulation fixe les mécanismes à l'avance : elle sert à comprendre une méthode,
pas à découvrir une cause inconnue.

Dans une étude réelle, une différence entre deux groupes peut aussi venir du
plan d'échantillonnage, d'un biais de mesure ou d'une autre différence entre les
groupes. Le test de Welch répond à une question sur les moyennes de deux groupes
indépendants ; il ne compare pas toutes les caractéristiques des distributions
et ne démontre pas qu'une intervention a causé l'écart.
