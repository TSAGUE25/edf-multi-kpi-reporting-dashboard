import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def compute_kpis(df):
    """Compute aggregate KPIs per site and globally."""
    site_kpis = df.groupby(['site', 'type_energie']).agg(
        prod_totale_twh   = ('production_gwh', lambda x: x.sum() / 1000),
        dispo_moy_pct     = ('disponibilite_pct', 'mean'),
        cout_maint_total  = ('cout_maintenance_keur', 'sum'),
        nb_incidents_total= ('nb_incidents', 'sum'),
        co2_evite_kt      = ('co2_evite_kt', 'sum'),
        revenue_total_meur= ('revenue_meur', 'sum'),
    ).round(2).reset_index()

    global_kpis = {
        'prod_totale_twh':   df['production_gwh'].sum() / 1000,
        'revenue_total_meur': df['revenue_meur'].sum(),
        'dispo_moy':         df['disponibilite_pct'].mean(),
        'co2_evite_kt':      df['co2_evite_kt'].sum(),
        'nb_incidents':      df['nb_incidents'].sum(),
    }
    return site_kpis, global_kpis


def monthly_trend(df):
    return df.groupby(['year', 'month']).agg(
        production_gwh   = ('production_gwh', 'sum'),
        revenue_meur     = ('revenue_meur', 'sum'),
        disponibilite_pct= ('disponibilite_pct', 'mean'),
        nb_incidents     = ('nb_incidents', 'sum'),
    ).reset_index()


def energy_mix(df):
    return df.groupby('type_energie')['production_gwh'].sum()


def alert_sites(df, dispo_threshold=90, incident_threshold=5):
    recent = df[df['year'] == df['year'].max()]
    alerts = recent.groupby('site').agg(
        dispo_moy=('disponibilite_pct', 'mean'),
        incidents=('nb_incidents', 'sum'),
    )
    alerts['alerte_dispo']    = alerts['dispo_moy'] < dispo_threshold
    alerts['alerte_incidents'] = alerts['incidents'] > incident_threshold
    return alerts


def plot_executive_dashboard(df):
    site_kpis, global_kpis = compute_kpis(df)
    monthly = monthly_trend(df)
    mix     = energy_mix(df)
    monthly['period'] = monthly['year'].astype(str) + '-' + monthly['month'].astype(str).str.zfill(2)

    fig = plt.figure(figsize=(18, 12))
    gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.5, wspace=0.4)

    # Title banner
    fig.text(0.5, 0.97,
             f'Tableau de bord EDF — Production : {global_kpis["prod_totale_twh"]:.1f} TWh  '
             f'| Revenue : {global_kpis["revenue_total_meur"]:.0f} M€  '
             f'| Disponibilité : {global_kpis["dispo_moy"]:.1f}%  '
             f'| CO₂ évité : {global_kpis["co2_evite_kt"]:.0f} kt',
             ha='center', va='top', fontsize=11, fontweight='bold',
             color='white', bbox=dict(boxstyle='round', facecolor='#1976D2', alpha=0.9))

    # 1. Monthly production
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.plot(range(len(monthly)), monthly['production_gwh'], color='#2196F3', lw=2)
    ax1.fill_between(range(len(monthly)), monthly['production_gwh'], alpha=0.2)
    ax1.set_title('Production mensuelle totale (GWh)'); ax1.set_xlabel('Mois')
    ax1.set_xticks(range(0, len(monthly), 6))
    ax1.set_xticklabels(monthly['period'].iloc[::6], rotation=45, fontsize=8)

    # 2. Energy mix pie
    ax2 = fig.add_subplot(gs[0, 2])
    colors_mix = {'Nucleaire': '#5C6BC0', 'Eolien': '#26A69A', 'Solaire': '#FFA726'}
    ax2.pie(mix.values, labels=mix.index, autopct='%1.1f%%',
            colors=[colors_mix.get(k, 'grey') for k in mix.index])
    ax2.set_title('Mix énergétique')

    # 3. Production per site
    ax3 = fig.add_subplot(gs[1, 0])
    colors_bar = ['#5C6BC0' if t == 'Nucleaire' else '#26A69A' if t == 'Eolien' else '#FFA726'
                  for t in site_kpis['type_energie']]
    ax3.barh(site_kpis['site'], site_kpis['prod_totale_twh'], color=colors_bar)
    ax3.set_title('Production par site (TWh)'); ax3.set_xlabel('TWh')

    # 4. Availability per site
    ax4 = fig.add_subplot(gs[1, 1])
    colors_dispo = ['#4CAF50' if d >= 92 else '#FF9800' if d >= 85 else '#F44336'
                    for d in site_kpis['dispo_moy_pct']]
    ax4.barh(site_kpis['site'], site_kpis['dispo_moy_pct'], color=colors_dispo)
    ax4.axvline(90, color='red', ls='--', lw=1, label='Seuil 90%')
    ax4.set_title('Disponibilité moyenne (%)'); ax4.legend(fontsize=8)

    # 5. Monthly incidents
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.bar(range(len(monthly)), monthly['nb_incidents'], color='#EF5350', alpha=0.8)
    ax5.set_title('Incidents mensuels'); ax5.set_xlabel('Mois')

    # 6. Revenue trend
    ax6 = fig.add_subplot(gs[2, :2])
    ax6.bar(range(len(monthly)), monthly['revenue_meur'], color='#66BB6A', alpha=0.8)
    ax6.set_title('Revenu mensuel (M€)')
    ax6.set_xticks(range(0, len(monthly), 6))
    ax6.set_xticklabels(monthly['period'].iloc[::6], rotation=45, fontsize=8)

    # 7. Maintenance costs
    ax7 = fig.add_subplot(gs[2, 2])
    maint_site = df.groupby('site')['cout_maintenance_keur'].sum()
    ax7.pie(maint_site.values, labels=maint_site.index, autopct='%1.1f%%')
    ax7.set_title('Répartition coûts maintenance')

    plt.show()
