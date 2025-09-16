import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Pfad zum processed DataFrame (mit numerischen Features)
path = "../data/processed/test.csv"
df = pd.read_csv(path)

# 1) Target-Feature sicher numerisch machen (Bool -> 0/1)
if 'failure_after_7_days' in df.columns:
    # In vielen Fällen bereits 0/1 oder True/False
    df['failure_after_7_days'] = df['failure_after_7_days'].astype(bool).astype(int)
else:
    raise ValueError("Target-Spalte 'failure_after_7_days' nicht im DataFrame gefunden.")

# 2) Vorverarbeitung: Nur numerische Spalten verwenden
numeric_df = df.select_dtypes(include=[np.number]).copy()

print("Numerische Spalten:", numeric_df.columns.tolist())

# 3) Spearman-Korrelationsmatrix berechnen
corr = numeric_df.corr(method='spearman')

print("Spearman-Korrelationsmatrix.shape:", corr.shape)

# 4) Heatmap Visualisierung
plt.figure(figsize=(12, 10))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            vmin=-1, vmax=1, linewidths=0.5, cbar_kws={"label": "Spearman ρ"})
plt.title("Spearman-Korrelationsmatrix inkl. Target: failure_after_7_days")
plt.tight_layout()
heatmap_path = "../data/processed/spearman_corr_heatmap_with_target.png"
plt.savefig(heatmap_path, dpi=300)
plt.close()
print(f"Heatmap gespeichert: {heatmap_path}")

# 5) Relevanzmaß: durchschnittliche absolute Korrelation pro Feature mit allen anderen
abs_corr = corr.abs().copy()
np.fill_diagonal(abs_corr.values, 0)  # Diagonale auf 0 setzen, d.h. Selbstkorrelation ignorieren
feature_scores = abs_corr.mean(axis=0).sort_values(ascending=False)

print("\nDurchschnittliche absolute Korrelation pro Feature (Relevanzmaß):")
print(feature_scores)

# 6) Korrelationen zum Target separat (als Priorisierung)
if 'failure_after_7_days' in corr.columns:
    target_corr = corr['failure_after_7_days'].abs().drop('failure_after_7_days', errors='ignore')
    top_to_target = target_corr.sort_values(ascending=False)
    print("\nKorrelationen zum Target (failure_after_7_days):")
    print(top_to_target)

    top_n = 20
    print(f"\nTop {top_n} Merkmale nach Korrelation zum Target:")
    print(top_to_target.head(top_n))

# 7) Ergebnisse speichern
corr_path = "../data/processed/spearman_corr_matrix_with_target.csv"
corr.to_csv(corr_path)
print(f"Korrelationsmatrix gespeichert: {corr_path}")

scores_path = "../data/processed/feature_relevance_spearman_with_target.csv"
feature_scores.to_csv(scores_path, header=['avg_abs_rho'])
print(f"Feature-Relevanz gespeichert: {scores_path}")


'''
Wichtigsten:
time_diff_days        0.609160
InvSampTime           0.221232
OfsDevTight           0.187892
RadV_50per            0.183119
RawRadius             0.157726
InvSampTurn           0.145519
AmpDevStrict          0.140800
delta_RadV_50per      0.138530
RadV_25per            0.130835
delta_InvSampTime     0.126745
AmpSyncCheck          0.111223
OfsCos200             0.097210
delta_OfsDevTight     0.094835
ZpdReq                0.090311
OldFttiCheck          0.083806
ClCos300              0.083657
OfsCos100             0.081371
delta_RadV_25per      0.080642
delta_InvSampTurn     0.080002
delta_AmpDevStrict    0.078908
'''