import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Laden des Datensatzes
df = pd.read_csv("transformierte_normierte_daten.csv")

# source .venv/bin/activate.fish
# deactivate

# TODO Variablenauswahl!
# mit Random Forest oder Lasso


target_variable = "time_to_fail"
#df = df.drop(columns=['c_van17', 'c_serial_number', 'status_75'])

# Deskriptiv (summary, Lagemaße, Streumaße, Häufigkeiten)
# Lagemaße & Streumaße für numerische Variablen
numeric_vars = df.select_dtypes(include=['number']).columns

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