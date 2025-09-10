import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Laden des Datensatzes
df = pd.read_csv("transformierte_normierte_daten.csv")
print(df.head(10))

df = df[df['time_to_fail'] != 0]


# source .venv/bin/activate.fish
# deactivate

target_variable = "time_to_fail"
#df = df.drop(columns=['c_van17', 'c_serial_number', 'status_75'])

# Deskriptiv (summary, Lagemaße, Streumaße, Häufigkeiten)
# Lagemaße & Streumaße für numerische Variablen
numeric_vars = df.select_dtypes(include=['number']).columns

for var in numeric_vars:
    x = df[var].dropna()  # Entfernen von NA-Werten
    mad = (x - x.median()).abs().median()  # Manuelle Berechnung des MAD
    print(f"\nVariable: {var}")
    print(f"Mittelwert: {x.mean()}")
    print(f"Median: {x.median()}")
    print(f"Minimum: {x.min()}")
    print(f"Maximum: {x.max()}")
    print(f"25%-Quantil: {x.quantile(0.25)}")
    print(f"75%-Quantil: {x.quantile(0.75)}")
    print(f"Standardabweichung: {x.std()}")
    print(f"Interquartilsabstand (IQR): {x.quantile(0.75) - x.quantile(0.25)}")
    print(f"MAD: {mad}")
    print("\n------------------------\n")

# Häufigkeiten für kategoriale Variablen
categorical_vars = df.select_dtypes(include=['object', 'category']).columns

for var in categorical_vars:
    print(f"\n\nHäufigkeiten für Variable: {var}")
    print(df[var].value_counts())  # absolute Häufigkeiten
    print(df[var].value_counts(normalize=True))  # relative Häufigkeiten
    

# Explorative Analyse
for var in df.columns:
    x = df[var]
    
    # Numerische Variablen: Histogramm
    if pd.api.types.is_numeric_dtype(x):
        plt.figure(figsize=(8, 6))
        plt.hist(x.dropna(), bins=20, color='lightblue', edgecolor='black')
        plt.title(f"Histogram of {var}")
        plt.xlabel(var)
        plt.ylabel("Frequency")
        plt.savefig(f"histogram_{var}.png")
        plt.close()
    
    # Kategorische Variablen: Balkendiagramm
    elif pd.api.types.is_categorical_dtype(x) or pd.api.types.is_object_dtype(x):
        plt.figure(figsize=(8, 6))
        counts = x.value_counts()
        counts.plot(kind='bar', color='lightgreen')
        plt.title(f"Barplot of {var}")
        plt.xlabel(var)
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.savefig(f"barplot_{var}.png")
        plt.close()

# Numerische Einflussvariablen
for var in df.select_dtypes(include=['number']).columns:
    if var != target_variable:
        plt.figure(figsize=(8, 6))
        plt.scatter(df[var], df[target_variable], alpha=0.5)
        plt.title(f"Absenteeism by {var}")
        plt.xlabel(var)
        plt.ylabel(target_variable)
        plt.savefig(f"scatter_{var}.png")
        plt.close()

# Kategorische Einflussvariablen
for var in df.select_dtypes(include=['object', 'category']).columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[var], y=df[target_variable], showfliers=False)
    plt.title(f"Absenteeism Time by {var}")
    plt.xlabel(var)
    plt.ylabel(target_variable)
    plt.xticks(rotation=45)
    plt.savefig(f"boxplot_{var}.png")
    plt.close()


'''
# Berechnen der einzelnen Korrelationswerten jeder Einflussvariable mit der Zielvariable "time_to_fail"
pearson_corr = df.corr(method="pearson")[target_variable]
kendall_corr = df.corr(method="kendall")[target_variable]
spearman_corr = df.corr(method="spearman")[target_variable]

# Einfügen der Daten in einen pandas Dataframe zur besseren Auswertung
correlation_df = pd.DataFrame(
    {"Pearson": pearson_corr, "Kendall": kendall_corr, "Spearman": spearman_corr}
)
# Entfernen der Spalte "time_to_fail", da Korrelation zw der gleichen Variable immer den Wert 1.0 gibt
correlation_df = correlation_df.drop(target_variable)

# Ausgeben der 15 höchsten absoluten Korrelationswerte je Korrelationstyp
top_15_pearson = correlation_df["Pearson"].abs().nlargest(15)
top_15_kendall = correlation_df["Kendall"].abs().nlargest(15)
top_15_spearman = correlation_df["Spearman"].abs().nlargest(15)

print("Top 15 Features based on Pearson Correlation:")
print(top_15_pearson)

print("\nTop 15 Features based on Kendall Correlation:")
print(top_15_kendall)

print("\nTop 15 Features based on Spearman Correlation:")
print(top_15_spearman)

# Ausgeben einer Heatmap mit den einzelnen Korrelationen
plt.figure(figsize=(12, 7))
sns.heatmap(
    correlation_df,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    square=True,
    cbar_kws={"shrink": 0.8},
)

plt.title(f"Correlation Heatmap with respect to {target_variable}")
plt.show()


# Wir haben die Spearman Korrelation ausgewählt, da diese robust ist und am besten Korrelationswerte von nicht-linearen Zusammenhängen darstellt
# Ausgabe:
"""
Top 15 Features based on Pearson Correlation:
first_date_b75     0.321848
msg_timestamp      0.274578
InvSampTime        0.191080
OfsDevTight        0.162141
InvSampTurn        0.146057
AmpDevStrict       0.145159
RawRadius          0.134318
OfsCos100          0.123585
OfsCos200          0.117725
ClCos50            0.115071
AmpSyncCheck       0.114022
ClCos150           0.110854
ClCos300           0.109483
OfsSin200          0.108051
status_75_VALID    0.085823
Name: Pearson, dtype: float64
Top 15 Features based on Kendall Correlation:
InvSampTime        0.268758
RadV_50per         0.239345
OfsDevTight        0.234002
first_date_b75     0.230175
InvSampTurn        0.194731
RawRadius          0.191736
AmpDevStrict       0.187597
RadV_25per         0.181099
AmpSyncCheck       0.153443
OfsCos200          0.133383
msg_timestamp      0.127818
OfsCos100          0.114968
ClCos300           0.114464
OfsSin200          0.112990
status_75_VALID    0.110790
Name: Kendall, dtype: float64
Top 15 Features based on Spearman Correlation:
InvSampTime       0.384226
RadV_50per        0.352231
first_date_b75    0.329266
OfsDevTight       0.321224
InvSampTurn       0.277248
AmpDevStrict      0.271702
RadV_25per        0.267166
RawRadius         0.240427
AmpSyncCheck      0.194393
msg_timestamp     0.188542
OfsCos200         0.175269
OfsCos100         0.155231
ClCos300          0.154002
OfsSin200         0.151150
ClSin300          0.145341
Name: Spearman, dtype: float64
"""
'''