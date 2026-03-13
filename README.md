# 🏥 InsurFair — Analyse de Biais et Prédiction des Coûts d'Assurance Médicale

> Application interactive Streamlit d'analyse de fairness et de modélisation prédictive sur un dataset d'assurance médicale américaine.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E?logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/Licence-MIT-green)

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Structure du projet](#-structure-du-projet)
- [Installation](#-installation)
- [Lancement](#-lancement)
- [Pages de l'application](#-pages-de-lapplication)
- [Métriques de fairness](#-métriques-de-fairness)
- [Dataset](#-dataset)
- [Normes de codage](#-normes-de-codage)

---

## 🎯 Présentation

InsurFair est une application d'analyse de données qui explore les **biais potentiels** dans les algorithmes de tarification d'assurance médicale. Elle permet de :

- Visualiser la distribution des coûts d'assurance selon différents profils
- Détecter des biais statistiques sur des attributs sensibles (genre, âge, tabagisme)
- Entraîner et comparer plusieurs modèles de machine learning
- Mesurer la fairness des prédictions via des métriques standardisées

**Problématique :** Si les algorithmes de tarification reproduisent les biais présents dans les données historiques, certains groupes (femmes, seniors, fumeurs défavorisés) peuvent subir une **discrimination systémique** lors de la fixation de leurs primes d'assurance.

---

## ✨ Fonctionnalités

### 🎛 Filtres globaux (sidebar)
- Filtrage dynamique par genre, statut fumeur, région, tranche d'âge et plage de charges
- Tous les graphiques et KPI se mettent à jour en temps réel

### 📊 Visualisations
- **15+ graphiques interactifs** : histogrammes, boxplots, violin plots, scatter plots, heatmaps, bubble charts, radar charts
- Comparaisons multivariées croisées (genre × fumeur × âge)
- Carte thermique des coûts moyens par combinaison de variables

### ⚖️ Analyse de fairness
- Différence de parité démographique
- Ratio d'impact disparate (règle des 4/5)
- Radar de fairness multi-attributs
- Tableau récapitulatif des métriques par groupe

### 🤖 Modélisation
- 4 modèles comparables : Random Forest, Gradient Boosting, Régression Linéaire, Ridge
- Métriques : MAE, RMSE, R²
- Analyse des résidus
- Importance des variables
- Fairness appliquée aux prédictions du modèle

---

## 🗂 Structure du projet

```
insurance_app_v2/
│
├── app.py                  # Application principale Streamlit
├── insurance.csv           # Dataset Medical Insurance Cost
├── requirements.txt        # Dépendances Python
├── README.md               # Documentation
│
└── utils/
    ├── __init__.py
    └── fairness.py         # Métriques de fairness personnalisées
```

---

## ⚙️ Installation

### Prérequis

- Python 3.9 ou supérieur
- pip

### Étapes

**1. Cloner ou extraire le projet**

```bash
# Si depuis un ZIP
unzip insurance_app_v2.zip
cd insurance_app_v2
```

**2. Créer un environnement virtuel** *(recommandé)*

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

**3. Installer les dépendances**

```bash
pip install -r requirements.txt
```

---

## 🚀 Lancement

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

---

## 📄 Pages de l'application

### 🏠 Tableau de bord
Vue d'ensemble avec 10 KPI clés (coûts moyens par groupe, ratios, pourcentages), graphiques de distribution et tendances de coûts par âge.

### 🔍 Exploration
Analyse multivariée interactive avec choix des axes et de la variable de couleur. Comprend des scatter plots avec courbe LOWESS, violin plots, heatmaps croisées et bubble charts.

### ⚠️ Détection de Biais
Sélection de l'attribut sensible à analyser avec seuil DI configurable. Affiche le ratio d'impact disparate, la différence de parité, un radar de fairness et un tableau récapitulatif.

### 🤖 Modélisation
Sélection et comparaison de modèles, visualisation des prédictions vs valeurs réelles, analyse des résidus, importance des variables, et évaluation de la fairness sur les prédictions.

---

## 📐 Métriques de fairness

### Différence de parité démographique
Mesure l'écart de coût moyen entre le groupe le plus avantagé et le moins avantagé.

```
DPD = max(coût_moyen_groupe) - min(coût_moyen_groupe)
```

### Ratio d'impact disparate
Ratio entre le coût moyen du groupe défavorisé et celui du groupe de référence.

```
DI = coût_moyen(groupe_défavorisé) / coût_moyen(groupe_référence)
```

- **DI < 0.8** → Biais significatif (règle des 4/5)
- **DI ≥ 0.8** → Dans les limites acceptables

Ces métriques sont implémentées dans `utils/fairness.py`.

---

## 📁 Dataset

**Medical Insurance Cost** — disponible sur [Kaggle](https://www.kaggle.com/datasets/mirichoi0218/insurance)

| Colonne | Type | Description |
|---|---|---|
| `age` | int | Âge de l'assuré (18–64 ans) |
| `sex` | str | Genre : `male` / `female` |
| `bmi` | float | Indice de Masse Corporelle |
| `children` | int | Nombre d'enfants couverts |
| `smoker` | str | Statut fumeur : `yes` / `no` |
| `region` | str | Région géographique (4 zones US) |
| `charges` | float | Coût annuel d'assurance ($) — *variable cible* |

**Statistiques clés :**
- 1 338 assurés
- 20,3 % de fumeurs
- Coût moyen : ~$13 270
- Coût médian : ~$9 382

---

## 🧹 Normes de codage

Ce projet suit les conventions **PEP 8** pour Python :

- Indentation : 4 espaces
- Nommage : `snake_case` pour les variables et fonctions
- Type hints sur les fonctions utilitaires
- Docstrings sur les fonctions publiques
- Mise en cache des données avec `@st.cache_data`
- Séparation des responsabilités : logique de fairness isolée dans `utils/`

---

## 🛠 Dépendances principales

| Package | Version | Usage |
|---|---|---|
| `streamlit` | ≥ 1.32 | Interface web interactive |
| `pandas` | ≥ 2.0 | Manipulation des données |
| `numpy` | ≥ 1.24 | Calculs numériques |
| `plotly` | ≥ 5.18 | Visualisations interactives |
| `scikit-learn` | ≥ 1.3 | Modèles ML et métriques |

---

## 👤 Auteur

Projet réalisé dans le cadre d'une analyse de fairness en assurance médicale.

---

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

*Dataset source : [Kaggle — Medical Insurance Cost](https://www.kaggle.com/datasets/mirichoi0218/insurance)*
