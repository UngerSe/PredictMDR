import pandas as pd

def main():
    path = "data/raw/dataset.csv"

    df = pd.read_csv(path)

    print("Spalten:", df.columns.tolist())

    print("\nInfo:")
    print(df.info())

    print("\nErste Zeilen:")
    print(df.head())

    ts_cols = [c for c in df.columns if "time" in c.lower() or "timestamp" in c.lower()]
    if ts_cols:
        col = ts_cols[0]
        df[col] = pd.to_datetime(df[col], errors="coerce")
        print(f"\nConverted column '{col}' to datetime.")

    target_cols = [c for c in df.columns if "fail" in c.lower() or "time_to_fail" in c.lower()]
    if target_cols:
        print("\nGefundene potenzielle Zielspalten:", target_cols)

    nulls = df.isnull().sum().sort_values(ascending=False)
    print("\nNullwerte pro Spalte:")
    print(nulls)

    unique_ser = df["c_serial_number"].nunique()
    print(f"\nAnzahl eindeutiger Seriennummern: {unique_ser}")

    counts = df.groupby("c_serial_number").size().describe()
    print("\nMessungen pro Seriennummer (Deskriptives):")
    print(counts)

    processed_path = "data/processed/01_phase1_overview.csv"
    df.to_csv(processed_path, index=False)
    print(f"Zwischenergebnis gespeichert: {processed_path}")

if __name__ == "__main__":
    main()
