import pandas as pd 
import numpy as np 
from pathlib import Path
import matplotlib.pyplot as plt 
import seaborn as sns 

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
CODE_DATA_DIR = PROJECT_DIR / "TIPE_BDD_CODE"
RESULT_DIR = PROJECT_DIR / "TIPE_RESULT"


def verifier_colonnes(df, colonnes_attendues, nom_fichier):
    colonnes_manquantes = [col for col in colonnes_attendues if col not in df.columns]
    if colonnes_manquantes:
        raise KeyError(
            f"Colonnes manquantes dans {nom_fichier}: {colonnes_manquantes}"
        )


def vecteur_panneau(alpha_deg, beta_deg):
    alpha = np.radians(alpha_deg)
    beta = np.radians(beta_deg)
    return np.array([
        np.sin(beta) * np.sin(alpha),
        np.sin(beta) * np.cos(alpha),
        np.cos(beta),
    ])


def chercher_orientation_suiveur_max(ligne, alphas, betas, surface):
    meilleur_resultat = None

    for alpha_deg in alphas:
        for beta_deg in betas:
            up = vecteur_panneau(alpha_deg, beta_deg)
            dot = (
                ligne["Us_x"] * up[0]
                + ligne["Us_y"] * up[1]
                + ligne["Us_z"] * up[2]
            )
            puissance = ligne["E_W_m2"] * surface * max(0, dot)

            if meilleur_resultat is None or puissance > meilleur_resultat["P_t_W_suiveur"]:
                meilleur_resultat = {
                    "date_time": ligne["date_time"],
                    "alpha_suiveur_deg": alpha_deg,
                    "beta_suiveur_deg": beta_deg,
                    "dot_product_suiveur": dot,
                    "P_t_W_suiveur": puissance,
                }

    return meilleur_resultat



fichier_us = CODE_DATA_DIR / "BDD_VecteurUs_Mulhouse_2024.xlsx"
fichier_eclairement = CODE_DATA_DIR / "BDD_eclairement_Mulhouse_2024.xlsx"

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

df_eclairement["E_W_m2"] = (
    df_eclairement["Gb(i)"] + df_eclairement["Gd(i)"] + df_eclairement["Gr(i)"]
)

# Fusionner les vecteurs solaires avec l'eclairement
df = df_us.merge(
    df_eclairement[["date_time", "E_W_m2"]],
    on="date_time",
    how="left",
)
df = df.dropna(subset=["E_W_m2"]).copy()

# Definir orientation optimale
alpha_fixe_deg = 180
beta_fixe_deg = 45
surface = 1.8

Up = vecteur_panneau(alpha_fixe_deg, beta_fixe_deg)

# Calcul de la puissance instantanee
df["dot_product"] = df["Us_x"] * Up[0] + df["Us_y"] * Up[1] + df["Us_z"] * Up[2]
df["P_t_W"] = df["E_W_m2"] * surface * np.maximum(0, df["dot_product"])

# Export du calcul du panneau fixe
df.to_excel(RESULT_DIR / "puissance_instantanee.xlsx", index=False)

# Grille de recherche alpha-beta
alphas = np.arange(0, 181, 5)
betas = np.arange(0, 91, 5)

# Calcul du panneau mobile (suiveur) a chaque instant
resultats_suiveur = []

for _, ligne in df.iterrows():
    resultat_suiveur = chercher_orientation_suiveur_max(
        ligne,
        alphas,
        betas,
        surface,
    )
    resultats_suiveur.append(resultat_suiveur)

df_suiveur = pd.DataFrame(resultats_suiveur)

# Ajouter les resultats du suiveur a la table principale
df = df.merge(df_suiveur, on="date_time", how="left")

# Construire le fichier final avec les deux puissances a chaque instant
df["P_t_W_panneau_fixe"] = df["P_t_W"]
df["P_t_W_panneau_suiveur"] = df["P_t_W_suiveur"]

colonnes_finales = [
    "date_time",
    "elevation_deg",
    "azimuth_deg",
    "elevation_rad",
    "azimuth_rad",
    "Us_x",
    "Us_y",
    "Us_z",
    "E_W_m2",
    "dot_product",
    "dot_product_suiveur",
    "alpha_suiveur_deg",
    "beta_suiveur_deg",
    "P_t_W_panneau_fixe",
    "P_t_W_panneau_suiveur",
]

df_final = df[colonnes_finales].rename(columns={"date_time": "datetime_formatee"})

df_final.to_excel(RESULT_DIR / "puissance_instantanee_finale_2024.xlsx", index=False)

# Comparaison annuelle fixe / suiveur
energie_totale_fixe = df["P_t_W"].sum()
energie_totale_suiveur = df["P_t_W_suiveur"].sum()

comparaison_energies = pd.DataFrame([
    {
        "energie_totale_fixe_Wh": energie_totale_fixe,
        "energie_totale_suiveur_Wh": energie_totale_suiveur,
        "gain_suiveur_Wh": energie_totale_suiveur - energie_totale_fixe,
    }
])

comparaison_energies.to_excel(
    RESULT_DIR / "comparaison_energies_fixe_suiveur.xlsx",
    index=False,
)

print("Energie totale panneau fixe (Wh) :")
print(energie_totale_fixe)
print("Energie totale panneau suiveur (Wh) :")
print(energie_totale_suiveur)
