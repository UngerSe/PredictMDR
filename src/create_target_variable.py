import pandas as pd
from datetime import timedelta

# Daten laden
df = pd.read_csv("../data/raw/dataset.csv")

# Nur relevante Spalten behalten (optional, für Übersichtlichkeit)
df = df[['c_serial_number', 'msg_timestamp', 'status_75'] + [col for col in df.columns if col not in ['c_serial_number', 'msg_timestamp', 'status_75']]]

# Zeitstempel konvertieren (Millisekunden seit Unix-Epoch)
df['msg_timestamp'] = pd.to_datetime(df['msg_timestamp'], unit='ms', errors='coerce')

# Inkonsistente Daten (fehlende Werte) entfernen
df = df.dropna(subset=['c_serial_number', 'msg_timestamp', 'status_75'])

# Nach Seriennummer und Zeit sortieren
df = df.sort_values(['c_serial_number', 'msg_timestamp'])

# Zielvariable erzeugen
failure_after_7_days = []

for serial, group in df.groupby('c_serial_number'):
    group = group.reset_index(drop=True)
    # Finde den Index des Ausfalls (status_75 == "VALID") – es gibt pro Seriennummer nur einen
    fail_idx = group.index[group['status_75'] == "VALID"].tolist()
    if not fail_idx:
        # Kein Ausfall gefunden, alle False
        failure_after_7_days.extend([False] * len(group))
        continue
    fail_time = group.loc[fail_idx[0], 'msg_timestamp']
    for i, row in group.iterrows():
        time_diff = (fail_time - row['msg_timestamp']).total_seconds() / (60*60*24)
        is_failure_within_7_days = (0 < time_diff <= 7)
        failure_after_7_days.append(is_failure_within_7_days)

df['failure_after_7_days'] = failure_after_7_days

df.to_csv("../data/processed/with_target.csv", index=False)
print("Neue Datei mit Zielvariable gespeichert: data/processed/with_target.csv")
