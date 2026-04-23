import pandas as pd
import numpy as np
import csv


df=pd.read_excel("Desktop/TIPE/SunEarthTools_AnnualSunPath_2024_exc.xlsx")
df.to_csv("data.csv", index=False)
with open('data.csv', mode='r') as file:
    reader = csv.reader(file)
    jours_data = []


    for L in reader:
        print(L)

"Desktop/TIPE/SunEarthTools_AnnualSunPath_2024_Résultats_exc.xlsx"

"Desktop/TIPE/SunEarthTools_AnnualSunPath_2024_exc.xlsx"

def calculer_inclinaison_panneau(fichier_excel, fichier_sortie):
    # Charger le fichier Excel
    xls = pd.ExcelFile(fichier_excel)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0], skiprows=1)  # Suppression des premières lignes inutiles

    # Nettoyage des colonnes (les noms doivent être reconstruits)
    heures = df.iloc[0]  # La première ligne après le skip contient les noms des colonnes
    df = df[1:].reset_index(drop=True)  # Supprimer cette ligne des données principales
    df.columns = heures  # Renommer les colonnes

    # Extraction des colonnes d'élévation (E) uniquement
    colonnes_elevation = [col for col in df.columns if isinstance(col, str) and col.startswith('E')]
    df_elevation = df[colonnes_elevation].apply(pd.to_numeric, errors='coerce')  # Convertir en nombres

    # Calcul de l'élévation moyenne en ignorant les valeurs manquantes
    elevation_moyenne = df_elevation.mean().mean()

    # Calcul de l'inclinaison optimale
    inclinaison_optimale = elevation_moyenne  # Approche simple : moyenne des élévations

    # Sauvegarde du résultat dans un fichier Excel
    df_resultat = pd.DataFrame({'Inclinaison Optimale': inclinaison_optimale})
    df_resultat.to_excel(fichier_sortie, index=False)

    return inclinaison_optimale



# Exemple d'utilisation
fichier_excel = "SunEarthTools_AnnualSunPath_2024_exc.xlsx"
fichier_sortie = "Inclinaison_Optimale.xlsx"
inclinaison = calculer_inclinaison_panneau(fichier_excel, fichier_sortie)
print(f"L'angle optimal pour fixer le panneau est : {inclinaison:.2f}°")



Ur=[cos(b)*cos(a),cos(b)*sin(a),sin(b)]
Us=[cos(c)*cos(d),cos(c)*sin(d),sin(c)]

 np.dot(Ur,Us)  # Calcul du produit scalaire







