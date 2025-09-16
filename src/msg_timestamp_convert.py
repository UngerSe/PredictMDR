import pandas as pd
import numpy as np


def main():
    # CSV einlesen
    df = pd.read_csv("../data/raw/dataset.csv")

    # Übersicht über msg_timestamp
    print("Beispielwerte für msg_timestamp:", df['msg_timestamp'].head(10).tolist())
    print("Min:", df['msg_timestamp'].min())
    print("Max:", df['msg_timestamp'].max())

    # Probiere verschiedene Einheiten aus (Sekunden, Millisekunden, Mikrosekunden)
    # Vermutlich ist es ein Unix-Timestamp in Millisekunden:
    df['datetime_ms'] = pd.to_datetime(df['msg_timestamp'], unit='ms', errors='coerce')
    print("\nKonvertiert mit unit='ms':")
    print(df['datetime_ms'].describe())

    # Alternativ: in Sekunden?
    df['datetime_s'] = pd.to_datetime(df['msg_timestamp'], unit='s', errors='coerce')
    print("\nKonvertiert mit unit='s':")
    print(df['datetime_s'].describe())

    # Alternativ: in Mikrosekunden?
    df['datetime_us'] = pd.to_datetime(df['msg_timestamp'], unit='us', errors='coerce')
    print("\nKonvertiert mit unit='us':")
    print(df['datetime_us'].describe())

    # Ergebnis prüfen: Welche Konvertierung ergibt plausible Datumswerte?
    # Optional: Nur eine Vorschau speichern
    preview_cols = ['msg_timestamp', 'datetime_ms', 'datetime_s', 'datetime_us']
    df[preview_cols].head(50).to_csv("data/processed/timestamp_preview.csv", index=False)
    print("\nVorschau gespeichert unter: data/processed/timestamp_preview.csv")


if __name__ == "__main__":
    main()
