import pandas as pd

def main():
    path = "../data/raw/dataset.csv"

    df = pd.read_csv(path)

    print("Spalten:", df.columns.tolist())

    print("\nInfo:")
    print(df.info())

    print("\nErste Zeilen:")
    first_row_items = list(df.iloc[0].items())
    print(first_row_items)
    print(df.head())

    df['msg_timestamp'] = pd.to_datetime(df['msg_timestamp'], unit='ms', errors='coerce')
    print(f"\nConverted column '{'msg_timestamp'}' to datetime.")
    print(df['msg_timestamp'].isna().sum(), "ungültige Zeitstempel")
    print(df['msg_timestamp'].min(), df['msg_timestamp'].max())

    nulls = df.isnull().sum().sort_values(ascending=False)
    print("\nNullwerte pro Spalte:")
    print(nulls)

    unique_ser = df["c_serial_number"].nunique()
    print(f"\nAnzahl eindeutiger Seriennummern: {unique_ser}")

    counts = df.groupby("c_serial_number").size().describe()
    print("\nMessungen pro Seriennummer (Deskriptives):")
    print(counts)

    df_valid_time = df.dropna(subset=['msg_timestamp'])
    df_sorted = df_valid_time.sort_values(['c_serial_number', 'msg_timestamp'])

    # Zeitdifferenz zur vorherigen Messung innerhalb derselben Komponente
    df_sorted['delta_seconds'] = df_sorted.groupby('c_serial_number')['msg_timestamp'] \
        .diff().dt.total_seconds()

    # Durchschnittliches Intervall pro Komponente
    avg_interval_per_comp = df_sorted.groupby('c_serial_number')['delta_seconds'] \
        .mean().rename('avg_interval_seconds')

    print("\nDurchschnittliches Intervall (in Sekunden) pro Komponente:")
    print(avg_interval_per_comp)

    # Gesamtdurchschnitt der komponentenweisen Durchschnitte
    overall_component_avg = avg_interval_per_comp.mean()
    # Standardabweichung der komponentenweisen Durchschnitte
    std_of_component_avgs = avg_interval_per_comp.std()

    print("\nGesamtdurchschnitt der komponentenweisen Durchschnitte (mean):", overall_component_avg)
    print("Standardabweichung der komponentenweisen Durchschnitte (std):", std_of_component_avgs)

    processed_path = "../data/processed/01_phase1_overview.csv"
    df.to_csv(processed_path, index=False)
    print(f"Zwischenergebnis gespeichert: {processed_path}")

if __name__ == "__main__":
    main()
