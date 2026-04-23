import pandas as pd # type: ignore
import numpy as np # type: ignore
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "TIPE_Version F"
CODE_DATA_DIR = DATA_DIR / "BDD_TIPE_CODE"
RESULT_DIR = DATA_DIR / "TIPE_RESULT"


def verifier_colonnes(df, colonnes_attendues, nom_fichier):
    colonnes_manquantes = [col for col in colonnes_attendues if col not in df.columns]
    if colonnes_manquantes:
        raise KeyError(
            f"Colonnes manquantes dans {nom_fichier}: {colonnes_manquantes}"
        )

# Charger les fichiers de travail
fichier_us = CODE_DATA_DIR / "BDD_VecteurUs_Mulhouse_2024.xlsx"
fichier_eclairement = CODE_DATA_DIR / "BDD_eclairement_Mulhouse_2024.xlsx"
fichier_puissance_finale = RESULT_DIR / "puissance_instantanee_finale_2024.xlsx"

df_us = pd.read_excel(fichier_us)
df_eclairement = pd.read_excel(fichier_eclairement)

verifier_colonnes(
    df_us,
    ["date_time", "Us_x", "Us_y", "Us_z"],
    fichier_us.name,
)
verifier_colonnes(
    df_eclairement,
    ["date_time", "Gb(i)", "Gd(i)", "Gr(i)"],
    fichier_eclairement.name,
)

# Reconstituer l'eclairement total sur chaque pas de temps
df_eclairement["E_W_m2"] = (
    df_eclairement["Gb(i)"] + df_eclairement["Gd(i)"] + df_eclairement["Gr(i)"]
)

# Fusionner les vecteurs solaires avec l'eclairement
df = df_us.merge(
    df_eclairement[["date_time", "E_W_m2"]],
    on="date_time",
    how="left",
)

# Définir orientation optimale
alpha = np.radians(180)
beta = np.radians(45)
surface = 1.8

Up = np.array([
    np.sin(beta) * np.sin(alpha),
    np.sin(beta) * np.cos(alpha),
    np.cos(beta)])

# Calcul de la puissance instantanée
df["dot_product"] = df["Us_x"] * Up[0] + df["Us_y"] * Up[1] + df["Us_z"] * Up[2]
df["P_t_W"] = df["E_W_m2"] * surface * np.maximum(0, df["dot_product"])

# Export du fichier
df.to_excel(RESULT_DIR / "puissance_instantanee.xlsx", index=False)

##________________________________________________________

alphas = np.arange(0, 181, 5)
betas = np.arange(0, 91, 5)

resultats_suiveur = []

for _, ligne in df.iterrows():
    puissance_max = -1
    alpha_optimal = None
    beta_optimal = None
    dot_optimal = None

    for alpha_deg in alphas:
        for beta_deg in betas:
            alpha = np.radians(alpha_deg)
            beta = np.radians(beta_deg)
            Up = np.array([
                np.sin(beta) * np.sin(alpha),
                np.sin(beta) * np.cos(alpha),
                np.cos(beta)])

            dot = (
                ligne["Us_x"] * Up[0]
                + ligne["Us_y"] * Up[1]
                + ligne["Us_z"] * Up[2]
            )
            puissance = ligne["E_W_m2"] * surface * max(0, dot)

            if puissance > puissance_max:
                puissance_max = puissance
                alpha_optimal = alpha_deg
                beta_optimal = beta_deg
                dot_optimal = dot

    resultats_suiveur.append({
        "date_time": ligne["date_time"],
        "alpha_suiveur_deg": alpha_optimal,
        "beta_suiveur_deg": beta_optimal,
        "dot_product_suiveur": dot_optimal,
        "P_t_W_suiveur": puissance_max,
    })

df_suiveur = pd.DataFrame(resultats_suiveur)
df = df.merge(df_suiveur, on="date_time", how="left")

df.to_excel(RESULT_DIR / "puissance_instantanee_avec_suiveur.xlsx", index=False)
