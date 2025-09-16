import pandas as pd
import numpy as np

# Daten laden
df = pd.read_csv("../data/raw/dataset.csv")

# Relevante Spalten auswählen
relevant = ['c_serial_number', 'msg_timestamp', 'status_75'] + \
    [c for c in df.columns if c not in ['c_serial_number', 'msg_timestamp', 'status_75']]
df = df[relevant]

# Zeitstempel konvertieren (ms -> datetime)
df['msg_timestamp'] = pd.to_datetime(df['msg_timestamp'], unit='ms', errors='coerce')

# Inkonsistente Daten entfernen
df = df.dropna(subset=['c_serial_number', 'msg_timestamp', 'status_75'])

# Nach Seriennummer und Zeit sortieren
df = df.sort_values(['c_serial_number', 'msg_timestamp'])

# Numerische Spalten identifizieren (inkl. Delta später)
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
key_cols = {'c_serial_number', 'msg_timestamp'}
numeric_cols = [c for c in numeric_cols if c not in key_cols]

# Prev-Spalten erstellen (ein Schritt)
prev = df.groupby('c_serial_number')[numeric_cols].shift(1)

# Delta-Spalten als DataFrame erzeugen
delta = df[numeric_cols] - prev
delta.columns = [f"delta_{c}" for c in numeric_cols]

# Prev-Spalten nicht mehr benötigt, Delta-Spalten anhängen
df = pd.concat([df, delta], axis=1)

# Zielvariable erzeugen (Ausfall innerhalb von 7 Tagen nach Messzeitpunkt)
failure_after_7_days = []
for serial, group in df.groupby('c_serial_number'):
    grp = group.reset_index(drop=True)
    fail_idx = grp.index[grp['status_75'] == "VALID"].tolist()
    if not fail_idx:
        failure_after_7_days.extend([False] * len(grp))
        continue
    fail_time = grp.loc[fail_idx[0], 'msg_timestamp']
    for i, row in grp.iterrows():
        time_diff = (fail_time - row['msg_timestamp']).total_seconds() / 86400.0
        failure_after_7_days.append(0 < time_diff <= 7)

df['failure_after_7_days'] = failure_after_7_days

# Ergebnis speichern
df.to_csv("../data/processed/with_target_and_delta.csv", index=False)
print("Datei gespeichert: data/processed/with_target_and_delta.csv")
