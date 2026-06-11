import numpy as np
import pandas as pd
from pathlib import Path


def generate_edf_kpi_data(n_months=60, seed=42):
    rng = np.random.default_rng(seed)

    dates = pd.date_range('2019-01-01', periods=n_months, freq='MS')
    sites = ['Centrale_A', 'Centrale_B', 'Centrale_C', 'Parc_Eolien_N', 'Parc_Solaire_S']
    types = ['Nucleaire', 'Nucleaire', 'Nucleaire', 'Eolien', 'Solaire']
    capacite_mw = [1450, 900, 1300, 320, 150]

    records = []
    for site, stype, cap in zip(sites, types, capacite_mw):
        # Seasonal production factor
        season = np.sin(2 * np.pi * np.arange(n_months) / 12) * 0.15
        if stype == 'Solaire':
            season = np.sin(2 * np.pi * (np.arange(n_months) - 3) / 12) * 0.35
        elif stype == 'Eolien':
            season = -np.sin(2 * np.pi * (np.arange(n_months) - 2) / 12) * 0.20

        prod_factor = np.clip(0.75 + season + rng.normal(0, 0.05, n_months), 0.20, 0.98)
        production_gwh = (cap * prod_factor * 24 * 30 / 1000).round(1)

        disponibilite_pct = np.clip(
            (97 if stype == 'Nucleaire' else 90) + rng.normal(0, 2, n_months), 50, 100
        ).round(1)

        cout_maintenance_keur = np.clip(
            rng.lognormal(3.5, 0.5, n_months) * (cap / 1000), 5, 500
        ).round(1)

        incidents = rng.poisson(0.8 if stype == 'Nucleaire' else 1.5, n_months)
        co2_evite_kt = (production_gwh * 0.42).round(1) if stype != 'Nucleaire' else np.zeros(n_months)

        prix_mwh = np.clip(45 + 20 * np.sin(2 * np.pi * np.arange(n_months) / 12)
                           + rng.normal(0, 8, n_months), 20, 120).round(2)

        revenue_meur = (production_gwh * prix_mwh / 1000).round(2)

        for i, d in enumerate(dates):
            records.append({
                'date': d,
                'year': d.year,
                'month': d.month,
                'site': site,
                'type_energie': stype,
                'capacite_mw': cap,
                'production_gwh': production_gwh[i],
                'disponibilite_pct': disponibilite_pct[i],
                'cout_maintenance_keur': cout_maintenance_keur[i],
                'nb_incidents': incidents[i],
                'co2_evite_kt': co2_evite_kt[i],
                'prix_mwh': prix_mwh[i],
                'revenue_meur': revenue_meur[i],
            })

    return pd.DataFrame(records)


def load_or_generate(csv_path, n_months=60, seed=42):
    path = Path(csv_path)
    if path.exists():
        return pd.read_csv(path, parse_dates=['date'])
    df = generate_edf_kpi_data(n_months=n_months, seed=seed)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df
