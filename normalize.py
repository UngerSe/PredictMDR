import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Laden des Datensatzes
df = pd.read_csv("prep_dataset.csv")

# Liste der relevanten Variablen, die transformiert werden sollen
transform_variables = [
    "AmpDevStrict", "AmpSyncCheck", "ClCos150", "ClCos300", 
    "ClSin150", "ClSin300", "InvSampTime", "InvSampTurn",
    "mileage", "OfsCos100", "OfsCos200", "OfsDevTight",
    "OfsSin100", "OfsSin200", "RadV_25per", "RadV_50per",
    "RawRadius","time_to_fail", "EcuLifeT"
]

# Logarithmische Transformation der ausgewählten Variablen
for var in transform_variables:
    df[var] = df[var].apply(lambda x: np.log(x + 1))  # +1 um log(0) zu vermeiden

# Liste der relevanten Variablen, die normiert werden sollen
norm_variables = [
    "AmpDevStrict", "AmpSyncCheck", "ClCos150", "ClCos300", 
    "ClSin150", "ClSin300", "InvSampTime", "InvSampTurn", 
    "mileage", "OfsCos100", "OfsCos200", "OfsDevTight",
    "OfsSin100", "OfsSin200", "RadV_25per", "RadV_50per", 
    "RawRadius", "EcuLifeT", "time_to_fail", "sick_time"
]

# StandardScaler initialisieren
scaler = StandardScaler()

# Normieren der ausgewählten Variablen
#df[norm_variables] = scaler.fit_transform(df[norm_variables])

# Die transformierten und normierten Daten in einer neuen Datei speichern
df.to_csv("transformierte_normierte_daten.csv", index=False)

print("Die relevanten Variablen wurden transformiert und normiert und in 'transformierte_normierte_daten.csv' gespeichert.")
