import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier  # Beispielmodell

# Schritt 1: Daten laden und Features bestimmen
df = pd.read_csv('../data/processed/test.csv')

group_col = 'c_serial_number'
time_col = 'msg_timestamp'
target_col = 'failure_after_7_days'
feature_cols = [c for c in df.columns if c not in [group_col, time_col, target_col]]

# Schritt 2: Zeitbasierten Split pro Gruppe (wie oben erarbeitet)
df_sorted = df.sort_values([group_col, time_col]).copy()
train_frac = 0.8  # 80% Training, 20% Test

train_indices = []
test_indices = []

for g, grp in df_sorted.groupby(group_col):
    n = len(grp)
    if n == 0:
        continue
    k_train = max(1, int(n * train_frac))
    train_idx_grp = grp.index[:k_train]
    test_idx_grp = grp.index[k_train:]
    train_indices.extend(train_idx_grp.tolist())
    test_indices.extend(test_idx_grp.tolist())

df_train = df_sorted.loc[train_indices]
df_test = df_sorted.loc[test_indices]

X_train = df_train[feature_cols]
y_train = df_train[target_col]
X_test = df_test[feature_cols]
y_test = df_test[target_col]

# Optional: Balancing des Trainingsdatensatzes (Oversampling der True-Klasse)
from sklearn.utils import resample

train_df = pd.concat([X_train, y_train.rename(target_col)], axis=1)
df_false = train_df[train_df[target_col] == 0]
df_true  = train_df[train_df[target_col] == 1]
n_target = max(len(df_false), len(df_true))
df_true_oversampled = resample(df_true, replace=True, n_samples=n_target, random_state=42)
train_balanced = pd.concat([df_false, df_true_oversampled])
X_train_balanced = train_balanced[feature_cols]
y_train_balanced = train_balanced[target_col]

# Schritt 3: Modell trainieren (Beispiel: RandomForest)
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train_balanced, y_train_balanced)

# Schritt 4: Vorhersage auf neuen Komponentenlogs
# Angenommen, new_logs ist das DataFrame mit neuen Logdaten ohne target_col
# Beispiel: new_logs = pd.read_csv('../data/processed/new_logs.csv')
# Hier als Platzhalter: new_logs = df_test.drop(columns=target_col)
# (In der Praxis sind das die neuen, zu bewertenden Komponenten)

# Annahme: new_logs enthält alle Features wie feature_cols
# Im Beispiel verwenden wir X_test als Proxy für neue Daten
new_logs = X_test.copy()

# Wahrscheinlichkeiten für Ausfall vorhersagen
probs = clf.predict_proba(new_logs)[:, 1]
new_logs = new_logs.copy()
new_logs['predicted_failure_prob'] = probs

# Schritt 5: Auswahl der Komponenten mit durchschnittlicher Wahrscheinlichkeit ca. 10%
new_logs_sorted = new_logs.sort_values('predicted_failure_prob', ascending=False).reset_index(drop=True)
cum_mean = new_logs_sorted['predicted_failure_prob'].expanding().mean()
idx = np.argmax(cum_mean <= 0.10)

# Die ausgewählten Komponenten
selected = new_logs_sorted.iloc[:idx+1]
print(f"Durchschnittliche Wahrscheinlichkeit: {selected['predicted_failure_prob'].mean():.4f}")
print(f"Anzahl ausgewählter Komponenten: {len(selected)}")

# Optional: Ausgabe der ausgewählten Komponenten
# selected.to_csv('komponenten_zur_praeventiven_wartung.csv', index=False)
