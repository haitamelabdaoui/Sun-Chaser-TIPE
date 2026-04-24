# Sun-Chaser — Solar Panel Orientation Optimization

> **TIPE Research Project** | Lycée Albert Schweitzer, Mulhouse, France | 2024–2025  
> *Presented to the jury of Concours Communs Polytechniques (CCP)*



## Research Question

**Which orientation maximizes the energy yield of a photovoltaic panel?**  
What are the trade-offs between fixed and sun-tracking systems in terms of efficiency, cost, and environmental impact?



## Objective

Compare the annual energy output of:
- A **fixed photovoltaic panel** (azimuth α = 180°, tilt β = 45°)
- A **sun-tracking system** that dynamically adjusts α and β in real time

Using real solar irradiance and sun position data for **Mulhouse, Alsace, France (2024)**.



## Key Result

> **+19.85% annual energy gain** achieved by the sun-tracking system over the fixed panel



## Methodology

### 1. Data
- `BDD_eclairement_Mulhouse_2024.csv` — Hourly solar irradiance (W/m²) over the full year 2024 in Mulhouse
- `BDD_VecteurUs_Mulhouse_2024.csv` — Hourly sun position vectors (azimuth & elevation) over the full year 2024

*Source: [SunEarthTools](https://www.sunearthtools.com/index.php)*

### 2. Core Algorithm
The power captured by a panel is proportional to the **dot product** between:
- The **sun direction vector** (from sun position data)
- The **panel normal vector** (defined by angles α and β)

```
P(t) ∝ max(0, sun_vector(t) · panel_vector(α, β))
```

### 3. Fixed Panel
Compute instantaneous and annual power output for a fixed panel at α = 180°, β = 45°.

### 4. Sun-Tracking Optimization
Run a nested `for` loop over all (α, β) angle combinations to find the pair that maximizes annual energy capture. Then generating a **heatmap** of energy yield across the angle space.

### 5. Results
- `TIPE_RESULT_F.csv` — Full comparison table with hourly power for both systems + annual energy sums
- `TIPE_heatmap.png` — Optimal angle range visualization
- `Optimisation de l’Orientation des Panneaux Solaires Photovoltaïques.pdf` — Complete study including economic, environmental, and technical analysis



## Tech Stack

- Python -> Core simulation & optimization 
- NumPy -> Vector operations & dot product computation 
- Pandas -> Data loading and processing 
- Matplotlib -> Heatmap 


## How to Run

```bash
# Install dependencies
pip install numpy pandas matplotlib

# Run the simulation
programme python - TIPE.py
```

The script produces:
- `TIPE_RESULT_F.csv` —> Hourly data table containing:
  - Sun position vectors (Us_x, Us_y, Us_z)
  - Irradiance E (W/m²)
  - Dot product & instantaneous power for the **fixed panel** (P_t_W_fixe)
  - Optimal tracking angles (alpha_suiveur_deg, beta_suiveur_deg)
  - Dot product & instantaneous power for the **tracking system** (P_t_W_suiveur)
  - Annual energy sums and **+19.85% gain** computation
- `TIPE_heatmap.png` —> Annual energy yield (Wh) across all (azimuth, tilt) combinations

## References

1. Jacques Bernard — *Génie Énergétique, Énergie solaire : calculs et optimisation*, Ellipses
2. Anne Labouret, Michel Villoz — *Énergie Solaire Photovoltaïque*, Dunod
3. SunEarthTools — https://www.sunearthtools.com
4. Gianni Pascoli — *Éléments de Mécanique Céleste*, Masson

## Author

**El Abdaoui Mohamed Haitam**  
Engineering Student @ IMT Mines Albi | Renewable Energy & GreenTech  
[LinkedIn](https://www.linkedin.com/in/haitam-el-abdaoui-129296254)
