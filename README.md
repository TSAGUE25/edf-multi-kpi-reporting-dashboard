# Reporting Multi-KPIs — Tableau de Bord Opérationnel

> **Piloter la performance opérationnelle par les indicateurs dans un contexte énergie/industrie**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Domaine](https://img.shields.io/badge/Domaine-Business%20Intelligence-green)
![Statut](https://img.shields.io/badge/Statut-Portfolio-orange)
![Données](https://img.shields.io/badge/Données-Simulées%2FAnonymisées-lightgrey)

---

## Contexte métier

Le pilotage opérationnel d'une organisation nécessite un suivi régulier de multiples indicateurs de performance. Un tableau de bord KPI permet de détecter rapidement les dérives et de déclencher les actions correctives.

---

## Problème traité

Construire un pipeline de calcul automatique de 15 KPIs opérationnels depuis des sources multiples, avec un système d'alertes sur seuils (CRITIQUE / ATTENTION) et une visualisation claire.

---

## Solution proposée

Pipeline multi-sources Python : ingestion données tickets, calcul des 15 KPIs mensuels, moteur d'alertes configurable avec seuils CRITIQUE/ATTENTION, export Excel et visualisation matplotlib. Cas générique et anonymisé.

---

## Technologies utilisées

| Outil | Usage |
|-------|-------|
| Python 3.10+ | Langage principal |
| pandas / numpy | Manipulation des données |
| scikit-learn | Machine Learning & preprocessing |
| matplotlib / seaborn | Visualisation |
| Jupyter Notebook | Exploration interactive |

> Voir `requirements.txt` pour la liste complète.

---

## Structure du projet

```
edf-multi-kpi-reporting-dashboard/
├── README.md              ← Ce fichier
├── PORTFOLIO.md           ← Documentation complète du cas d'usage
├── .gitignore
├── requirements.txt
├── notebooks/             ← Jupyter Notebooks d'exploration
├── src/                   ← Code Python modulaire
├── data_sample/           ← Données simulées (anonymisées)
├── figures/               ← Graphiques et visualisations
├── reports/               ← Rapports et synthèses
└── docs/                  ← Documentation complémentaire
```

---

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/TSAGUE25/edf-multi-kpi-reporting-dashboard.git
cd edf-multi-kpi-reporting-dashboard

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate    # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer Jupyter
jupyter notebook
```

---

## Métriques clés (données simulées)

```
15 KPIs opérationnels : délai résolution, taux satisfaction, volume tickets, SLA
```

---

## Valeur métier

Détection proactive des dérives. Réduction du temps de reporting manuel.

---

## Limites

Données simulées. Pas de connexion temps réel.

---

## Prochaines améliorations

Connexion API temps réel. Dashboard Power BI interactif. Alertes email/Slack.

---

## Avertissement — Confidentialité

> **Toutes les données utilisées dans ce projet sont simulées, synthétiques ou anonymisées.**
> Aucune donnée réelle, confidentielle ou propriétaire n'est présente dans ce dépôt.
> Ce projet est un cas d'usage pédagogique à destination du portfolio professionnel d'Emmanuel TSAGUE.

---

## Auteur

**Emmanuel TSAGUE** — Data Scientist / Data Analyst
Domaine : Business Intelligence · Performance opérationnelle · Reporting
GitHub : [TSAGUE25](https://github.com/TSAGUE25)

> Voir [PORTFOLIO.md](PORTFOLIO.md) pour la documentation complète du cas d'usage (24 sections).
