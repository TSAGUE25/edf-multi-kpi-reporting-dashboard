# CAS D'USAGE 5 — Reporting Multi-KPIs
## Piloter la performance opérationnelle par les indicateurs dans un contexte énergie / industrie

> **Auteur :** TSAGUE EMMANUEL — Data Scientist / Data Analyst  
> **Domaine :** Business Intelligence, Performance opérationnelle, Pilotage  
> **Repository GitHub :** `multi-kpi-reporting-dashboard`  
> **Statut :** Portfolio — données simulées — cas générique et anonymisé  
> **Date :** Juin 2026

> **Important :** Ce cas est entièrement générique et anonymisé. Il ne repose sur aucune donnée confidentielle, aucun système interne et aucune information propriétaire d'une organisation réelle.

---
## 1. TITRE ET RÉSUMÉ EXÉCUTIF

**"Reporting multi-KPIs pour piloter la performance opérationnelle — Du tableau de bord Excel manuel au dashboard Power BI automatisé"**

> **KPI (Key Performance Indicator — Indicateur Clé de Performance) :** mesure quantifiable qui permet de suivre l'atteinte d'un objectif. Un bon KPI est mesurable, comparable dans le temps, actionnable et aligné sur un objectif stratégique.

Un manager opérationnel supervise des activités dispersées : délais de traitement, taux de conformité, charge d'activité, disponibilité des équipements, qualité documentaire, sécurité, alertes. Ces indicateurs viennent de sources différentes. Le projet automatise leur consolidation et leur restitution dans un dashboard décisionnel.

**Résultats hypothétiques :** 15 KPI consolidés automatiquement, reporting mensuel réduit de 6 heures à 20 minutes, 3 alertes critiques identifiées.

---
## 2. CONTEXTE MÉTIER

Dans toute organisation industrielle ou énergétique, le pilotage opérationnel repose sur des indicateurs qui mesurent la performance de l'activité quotidienne :

| Domaine | Indicateurs typiques |
|---------|---------------------|
| **Production / Activité** | Volume traité, taux d'avancement, backlog |
| **Qualité** | Taux de conformité, taux d'erreur, non-conformités |
| **Délais** | Délai moyen de traitement, % dans les délais |
| **Sécurité** | Taux d'accidents, presqu'accidents, observations |
| **Disponibilité équipements** | Taux de disponibilité, MTBF, MTTR |
| **Ressources humaines** | Charge, absentéisme, compétences |
| **Conformité réglementaire** | Taux de conformité documentaire, audits |
| **Budget** | Écart budget/réalisé, taux d'engagement |

> **Backlog :** file d'attente des tâches ou demandes en attente de traitement. Un backlog croissant signale une surcharge d'activité ou un problème de traitement.

> **MTBF (Mean Time Between Failures) :** durée moyenne entre deux pannes d'un équipement. Plus le MTBF est élevé, plus l'équipement est fiable.

> **MTTR (Mean Time To Repair) :** durée moyenne de réparation après une panne. Plus le MTTR est bas, plus la maintenance est réactive.

---
## 3. POURQUOI CE SUJET EXISTE

| Raison | Symptôme sans pilotage |
|--------|----------------------|
| Données dispersées | Chaque service a son propre fichier Excel |
| Pas de vue consolidée | Le manager ne voit jamais tous ses KPI en même temps |
| Reporting manuel | 6 heures par mois pour consolider les données |
| Indicateurs non définis | Chacun calcule son propre taux de conformité |
| Pas d'historique | Impossible de comparer avec le mois précédent |
| Alertes absentes | Les dérives passent inaperçues jusqu'à ce qu'elles deviennent critiques |

---
## 4. PROBLÈME MÉTIER

> "Mon reporting mensuel dure 6 heures. Je copie-colle des données de 8 fichiers Excel différents. Et malgré ça, j'ai des incohérences entre les chiffres de mes équipes."

**Défis :**
1. Définir précisément chaque KPI (que mesure-t-on exactement ?)
2. Identifier et connecter toutes les sources de données
3. Automatiser la consolidation mensuelle
4. Détecter automatiquement les dérives et alertes
5. Restituer de façon claire aux managers et équipes terrain
6. Maintenir le système dans le temps

---
## 5. OBJECTIFS DU PROJET

| Objectif | Description | Livrable |
|----------|-------------|----------|
| Définir | Dictionnaire de 15 KPI avec définition métier exacte | `dictionnaire_kpi.md` |
| Consolider | Pipeline Python qui agrège les données sources | Script automatisé |
| Visualiser | Dashboard Power BI interactif | Fichier `.pbix` |
| Alerter | Seuils d'alerte configurables | Tableau d'alertes |
| Historiser | Suivi de l'évolution dans le temps | Base de données locale |
| Documenter | Guide de mise à jour mensuelle | `README_usage.md` |

---
## 6. DONNÉES UTILISÉES

> **Données entièrement simulées — cas générique.**

**Sources simulées consolidées en une base analytique :**

| Source | Table simulée | Fréquence | KPI produits |
|--------|--------------|-----------|--------------|
| Système de ticketing | `tickets.csv` | Quotidienne | Délais, backlog, taux résolution |
| GMAO | `interventions.csv` | Quotidienne | MTBF, MTTR, disponibilité |
| Qualité | `non_conformites.csv` | Hebdomadaire | Taux NC, gravité |
| RH | `absences.csv` | Mensuelle | Absentéisme, charge |
| Budget | `budget_suivi.csv` | Mensuelle | Écart, engagement |
| Sécurité | `incidents_securite.csv` | Événementielle | Taux accident |

**Variables de la table principale `tickets.csv` :**

| Variable | Type | Description |
|----------|------|-------------|
| `id_ticket` | Entier | Identifiant du ticket |
| `date_ouverture` | Date | Date de création du ticket |
| `date_cloture` | Date | Date de résolution |
| `priorite` | Catégorie | P1 (critique) / P2 / P3 |
| `type_demande` | Catégorie | Incident, Demande, Question |
| `service_demandeur` | Texte | Service à l'origine |
| `agent_traitement` | Texte | Agent ou équipe en charge |
| `statut` | Texte | Ouvert, En cours, Clôturé |
| `delai_resolution_heures` | Numérique | Durée effective de résolution |
| `dans_delai_cible` | Booléen | Résolu dans le délai cible |
| `satisfaction_score` | Entier | Score 1-5 si évaluation |

---
## 7. PRÉPARATION DES DONNÉES

```python
import pandas as pd
import numpy as np
from datetime import date, timedelta
import random

np.random.seed(42)
random.seed(42)

def generer_tickets(n=2000, debut="2024-01-01", fin="2025-12-31"):
    """Génère un jeu de tickets simulés sur 2 ans."""
    dates = pd.date_range(debut, fin, periods=n)
    priorites  = random.choices(["P1","P2","P3"], weights=[10,40,50], k=n)
    types      = random.choices(["Incident","Demande","Question"],
                                weights=[30,50,20], k=n)
    services   = random.choices(
        ["Production","Maintenance","Qualité","RH","Finance"], k=n)
    agents     = random.choices([f"Agent_{i}" for i in range(1,11)], k=n)

    delais_cible = {"P1":4, "P2":24, "P3":72}  # en heures
    delais_reels = []
    for p in priorites:
        cible = delais_cible[p]
        ecart = np.random.normal(0, cible * 0.4)
        delais_reels.append(max(0.5, cible + ecart))

    df = pd.DataFrame({
        "id_ticket":                range(1, n+1),
        "date_ouverture":           dates,
        "priorite":                 priorites,
        "type_demande":             types,
        "service_demandeur":        services,
        "agent_traitement":         agents,
        "statut":                   random.choices(
            ["Clôturé","En cours","Ouvert"], weights=[80,12,8], k=n),
        "delai_resolution_heures":  [round(d,1) for d in delais_reels],
        "satisfaction_score":       random.choices(
            [1,2,3,4,5], weights=[5,10,20,35,30], k=n)
    })

    df["date_cloture"] = df["date_ouverture"] + pd.to_timedelta(
        df["delai_resolution_heures"], unit="h")
    df["dans_delai_cible"] = df.apply(
        lambda r: r["delai_resolution_heures"] <= delais_cible[r["priorite"]],
        axis=1)
    df["mois"] = df["date_ouverture"].dt.to_period("M").astype(str)
    df["annee"] = df["date_ouverture"].dt.year

    return df

df_tickets = generer_tickets()
df_tickets.to_csv("data_sample/tickets.csv", index=False)
```

---
## 8. MÉTHODES ET OUTILS

### A. Calcul automatique des KPI

```python
def calculer_kpis_mensuels(df_tickets, mois_cible=None):
    """Calcule les 15 KPI mensuels à partir des tickets."""

    if mois_cible:
        df = df_tickets[df_tickets["mois"] == mois_cible].copy()
    else:
        df = df_tickets.copy()

    kpis = {}

    # KPI 1 : Volume total de tickets
    kpis["volume_tickets"]          = len(df)

    # KPI 2 : Taux de résolution dans les délais
    kpis["taux_delai_pct"]          = round(
        df["dans_delai_cible"].mean() * 100, 1)

    # KPI 3 : Délai moyen de résolution (heures)
    kpis["delai_moyen_h"]           = round(
        df["delai_resolution_heures"].mean(), 1)

    # KPI 4 : Backlog en cours
    kpis["backlog_en_cours"]        = (df["statut"] == "En cours").sum()

    # KPI 5 : Taux de satisfaction (score ≥ 4)
    kpis["taux_satisfaction_pct"]   = round(
        (df["satisfaction_score"] >= 4).mean() * 100, 1)

    # KPI 6 : P1 traités dans les délais
    p1 = df[df["priorite"] == "P1"]
    kpis["taux_p1_delai_pct"]       = round(
        p1["dans_delai_cible"].mean() * 100, 1) if len(p1) > 0 else 0

    # KPI 7 : Volume par service (top service)
    top_service = df["service_demandeur"].value_counts().idxmax()
    kpis["top_service_demandeur"]   = top_service

    # KPI 8 : Variation vs mois précédent (si données dispo)
    kpis["variation_volume"]        = None  # Calculé dans le pipeline comparaison

    return kpis

# KPI par mois
kpis_par_mois = []
for mois in df_tickets["mois"].unique():
    kpis = calculer_kpis_mensuels(df_tickets, mois)
    kpis["mois"] = mois
    kpis_par_mois.append(kpis)

df_kpis = pd.DataFrame(kpis_par_mois).sort_values("mois")
df_kpis.to_csv("reports/kpis_mensuels.csv", index=False)
```

### B. Système d'alertes automatiques

```python
def detecter_alertes(df_kpis, seuils=None):
    """
    Détecte les KPI qui dépassent les seuils d'alerte.
    Retourne une liste d'alertes avec niveau de criticité.
    """
    if seuils is None:
        seuils = {
            "taux_delai_pct":       {"min": 80,  "niveau_alerte": "CRITIQUE"},
            "taux_satisfaction_pct":{"min": 75,  "niveau_alerte": "ATTENTION"},
            "backlog_en_cours":     {"max": 50,  "niveau_alerte": "ATTENTION"},
            "taux_p1_delai_pct":    {"min": 95,  "niveau_alerte": "CRITIQUE"},
            "delai_moyen_h":        {"max": 30,  "niveau_alerte": "ATTENTION"},
        }

    alertes = []
    dernier_mois = df_kpis.iloc[-1]

    for kpi, seuil in seuils.items():
        valeur = dernier_mois.get(kpi)
        if valeur is None:
            continue
        alerte = None
        if "min" in seuil and valeur < seuil["min"]:
            alerte = {
                "kpi":      kpi,
                "valeur":   valeur,
                "seuil":    seuil["min"],
                "type":     "En dessous du seuil minimum",
                "niveau":   seuil["niveau_alerte"],
                "mois":     dernier_mois["mois"]
            }
        elif "max" in seuil and valeur > seuil["max"]:
            alerte = {
                "kpi":      kpi,
                "valeur":   valeur,
                "seuil":    seuil["max"],
                "type":     "Au-dessus du seuil maximum",
                "niveau":   seuil["niveau_alerte"],
                "mois":     dernier_mois["mois"]
            }
        if alerte:
            alertes.append(alerte)
            print(f"[{alerte['niveau']}] {kpi} = {valeur} "
                  f"(seuil : {alerte['seuil']})")

    return pd.DataFrame(alertes)

df_alertes = detecter_alertes(df_kpis)
```

### C. Dashboard Power BI — Structure

```python
# Export des données pour Power BI
tables_export = {
    "kpis_mensuels":    df_kpis,
    "tickets_detail":   df_tickets,
    "alertes":          df_alertes,
}

for nom, df in tables_export.items():
    df.to_csv(f"reports/powerbi_{nom}.csv",
              index=False, encoding="utf-8-sig")
    print(f"Exporté : {nom} ({len(df)} lignes)")

# Structure du dashboard Power BI recommandée :
# Page 1 : Vue d'ensemble — KPI en carte (Card) + variation N-1
# Page 2 : Analyse des délais — histogrammes, courbes, par priorité
# Page 3 : Performance par service — barres, heatmap agents × mois
# Page 4 : Alertes actives — tableau filtré sur statut alerte
# Page 5 : Tendances — courbes évolution KPI sur 24 mois
```

---
## 9. DÉMARCHE ÉTAPE PAR ÉTAPE

```
ÉTAPE 1 : Ateliers de définition des KPI avec les métiers (2 jours)
ÉTAPE 2 : Inventaire des sources de données (1 jour)
ÉTAPE 3 : Pipeline Python de collecte et consolidation (2 jours)
ÉTAPE 4 : Calcul automatique des 15 KPI (1 jour)
ÉTAPE 5 : Configuration des seuils d'alerte (0,5 jour)
ÉTAPE 6 : Construction du dashboard Power BI (2 jours)
ÉTAPE 7 : Test et validation avec les équipes (1 jour)
ÉTAPE 8 : Documentation et guide d'utilisation (0,5 jour)
ÉTAPE 9 : Déploiement et formation (0,5 jour)
```

---
## 10. MÉTRIQUES

| KPI | Définition précise | Seuil vert | Seuil rouge |
|-----|--------------------|-----------|-------------|
| Taux délai global | % tickets résolus dans délai cible | > 85 % | < 75 % |
| Taux délai P1 | % tickets critiques dans délai | > 95 % | < 90 % |
| Délai moyen (h) | Moyenne des délais de résolution | < 24 h | > 48 h |
| Backlog en cours | Nb tickets non clôturés | < 30 | > 60 |
| Satisfaction | % scores ≥ 4/5 | > 80 % | < 65 % |
| Volume mensuel | Nb tickets ouverts | Stable ±20 % | +50 % vs mois précédent |
| Taux premier contact | % résolu sans réouverture | > 75 % | < 60 % |

---
## 11. RÉSULTATS SIMULÉS

| KPI | Valeur simulée | Tendance | Alerte |
|-----|----------------|----------|--------|
| Volume tickets/mois | 167 | Stable | — |
| Taux délai global | 82,3 % | -2 pts | ATTENTION |
| Taux délai P1 | 91,0 % | -4 pts | CRITIQUE |
| Délai moyen | 26,4 h | +3 h | ATTENTION |
| Backlog | 38 | +8 | — |
| Satisfaction | 78,5 % | Stable | — |

---
## 12. VALEUR MÉTIER

| Valeur | Avant | Après |
|--------|-------|-------|
| Temps reporting | 6 heures/mois | 20 minutes |
| Visibilité | Fragmentée, 8 fichiers | Centralisée, 1 dashboard |
| Alertes | Détection tardive | Alerte immédiate |
| Décisions | Réactives | Préventives |
| Communication | Réunion mensuelle avec tableaux statiques | Dashboard partagé en temps réel |

---
## 13. LIMITES

- La définition des KPI doit impliquer les métiers — risque de désaccord
- Les seuils d'alerte sont subjectifs — nécessitent validation terrain
- L'automatisation dépend de la stabilité des sources de données
- Un KPI en vert ne signifie pas qu'il n'y a pas de problème sous-jacent
- Risque de "KPI washing" : multiplier les indicateurs sans améliorer la performance

> **KPI washing :** dérive qui consiste à mesurer beaucoup d'indicateurs pour donner une impression de pilotage rigoureux, sans que ces indicateurs n'entraînent de réelles décisions ou améliorations.

---
## 14. AMÉLIORATIONS

- Connexion directe aux sources (API, SQL) — supprimer les fichiers CSV intermédiaires
- Alertes email automatiques (smtplib Python)
- Scoring de priorisation des tickets par ML
- Analyse prédictive du backlog (ARIMA/Prophet)
- Integration GMAO / ERP directe
- Reporting mobile (Power BI Mobile)
- Commentaires et annotations dans Power BI

---
## 15. ARCHITECTURE GITHUB

```
multi-kpi-reporting-dashboard/
├── README.md
├── requirements.txt
├── data_sample/
│   ├── tickets.csv
│   ├── interventions.csv
│   └── generate_data.py
├── src/
│   ├── kpi_calculator.py
│   ├── alert_engine.py
│   └── powerbi_exporter.py
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_calcul_kpis.ipynb
│   └── 03_alertes_dashboard.ipynb
├── reports/
│   ├── kpis_mensuels.csv
│   └── alertes_actives.csv
├── dashboards/
│   └── reporting_operationnel.pbix
└── docs/
    ├── dictionnaire_kpi.md
    └── guide_utilisation.md
```

---
## 22-23. COMPÉTENCES DÉMONTRÉES

| Compétence | Preuve | Valeur | Phrase CV |
|-----------|--------|--------|-----------|
| KPI design | 15 KPI définis et documentés | Pilotage orienté décision | "Définition et automatisation de KPI opérationnels" |
| Pipeline Python | Consolidation multi-sources | Gain de temps reporting | "Pipeline Python de consolidation multi-sources" |
| Power BI | Dashboard interactif 5 pages | Adoption par les équipes | "Dashboard Power BI multi-KPI avec alertes" |
| Moteur d'alertes | Seuils configurables | Détection précoce | "Système d'alertes automatiques sur indicateurs" |
| Communication | Guide, dictionnaire KPI | Adoption utilisateurs | "Documentation et formation aux tableaux de bord" |

---

*Fin du document — TSAGUE EMMANUEL — CAS 5 — Reporting Multi-KPIs*
---

## Contact & Liens

**TSAGUE EMMANUEL** - Data Scientist

| | |
|---|---|
| Email | [emmatsague@yahoo.fr](mailto:emmatsague@yahoo.fr) |
| LinkedIn | [emmanuel-tsague-114295414](https://www.linkedin.com/in/emmanuel-tsague-114295414) |
| GitHub | [github.com/TSAGUE25](https://github.com/TSAGUE25) |
| Formation | Datascientest 2024 |
| Experience | EDF MAD EDVANCE |
| Domaines | Machine Learning - Data Analysis - Energie |

---

> Toutes les donnees de ce depot sont simulees et anonymisees.  
> Aucune donnee reelle ou confidentielle n'est presente.
