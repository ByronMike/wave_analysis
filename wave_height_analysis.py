import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import linregress
from statsmodels.tsa.seasonal import STL


# Define the path to the NetCDF file
output_file = "/home/mauger/Projects/example-app/wave_height_data.nc"

# Check if the file exists
if os.path.exists(output_file):
    # Open the NetCDF file using xarray
    ds = xr.open_dataset(output_file)
    print("Dataset loaded successfully")
    print(ds)  # Optional: print dataset information for inspection

    # Extract the wave height (VHM0) and time data
    wave_heights = ds["VHM0"].values  # Wave height data (likely multi-dimensional)
    time = ds["time"].values  # Time data (likely multi-dimensional)

    # Print shapes of the arrays
    print(f"Shape of wave heights: {wave_heights.shape}")
    print(f"Shape of time: {time.shape}")

    # If wave heights are multi-dimensional, take the mean across lat and lon
    wave_heights_mean = wave_heights.mean(axis=(1, 2))  # Averaging over lat and lon dimensions

    # Convert time to pandas datetime
    time_dt = pd.to_datetime(time)

    # Create a DataFrame with the time and mean wave heights
    df = pd.DataFrame({"Time": time_dt, "Mean_Wave_Height": wave_heights_mean})

    # Set the 'Time' column as the index
    df.set_index("Time", inplace=True)

    # Resample the data by month-end (ME) and take the mean for each month
    df_monthly = df.resample('ME').mean()
    
        # Effectuer la régression linéaire
    # Utiliser 'time' converti en nombre de jours depuis le début pour la régression
    time_numeric = (df_monthly.index - df_monthly.index.min()).days
    slope, intercept, r_value, p_value, std_err = linregress(time_numeric, df_monthly["Mean_Wave_Height"])

    # Calculer la ligne de régression
    regression_line = slope * time_numeric + intercept

    # Plot the time series of monthly mean wave heights
    plt.figure(figsize=(12, 6))
    plt.plot(df_monthly.index, df_monthly["Mean_Wave_Height"], label="Monthly Mean Wave Height", color='b')
    plt.xlabel("Time (Year-Month)")
    plt.ylabel("Wave Height (m)")
    plt.title("Monthly Wave Height Trend (2000 - 2023)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
# Ajouter la courbe de régression
    plt.plot(df_monthly.index, regression_line, label=f"Tendance (Régression Linéaire)", color='r', linestyle='--')

    # Afficher le coefficient de régression et la p-value
    plt.text(0.05, 0.95, f"Slope: {slope:.4f}\nR²: {r_value**2:.4f}\nP-value: {p_value:.4f}",
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

    plt.tight_layout()  # Ajuster la mise en page pour éviter le chevauchement

    # Save the plot as a PNG file instead of showing it interactively
    plot_filename = "/home/mauger/Projects/example-app/wave_height_trends.png"
    plt.savefig(plot_filename)
    print(f"Plot saved as {plot_filename}")

    # Optionally, close the plot to free resources
    plt.close()

else:
    print(f"Error: {output_file} does not exist.")

if os.path.exists(output_file):
    # Ouvrir le fichier NetCDF avec xarray
    ds = xr.open_dataset(output_file)
    print("Dataset chargé avec succès")
    print(ds)  # Facultatif : imprimer les informations du dataset pour inspection

    # Extraire les données de hauteur des vagues (VHM0) et de temps
    wave_heights = ds["VHM0"].values  # Données de hauteur des vagues
    time = ds["time"].values  # Données de temps

    # Afficher les dimensions des tableaux
    print(f"Forme de wave heights: {wave_heights.shape}")
    print(f"Forme de time: {time.shape}")

    # Si les hauteurs de vagues sont multidimensionnelles, calculer la moyenne sur les dimensions lat et lon
    wave_heights_mean = wave_heights.mean(axis=(1, 2))  # Moyenne sur les dimensions lat et lon

    # Convertir le temps en format datetime de pandas
    time_dt = pd.to_datetime(time)

    # Créer un DataFrame avec le temps et les hauteurs moyennes des vagues
    df = pd.DataFrame({"Time": time_dt, "Mean_Wave_Height": wave_heights_mean})

    # Définir la colonne 'Time' comme index
    df.set_index("Time", inplace=True)

    # Resampler les données par fin de mois (ME) et calculer la moyenne pour chaque mois
    df_monthly = df.resample('ME').mean()

    # Décomposer la série temporelle pour enlever la saisonnalité
    stl = STL(df_monthly["Mean_Wave_Height"], seasonal=13)  # saisonnalité par période de 13 mois (environ 1 an)
    result = stl.fit()

    # Extraire les composants
    trend = result.trend  # Composant de tendance
    seasonal = result.seasonal  # Composant saisonnier
    residual = result.resid  # Composant résiduel (détrendé)

    # Tracer les données saisonnières corrigées (détrendées)
    plt.figure(figsize=(12, 6))
    plt.plot(df_monthly.index, residual, label="Saison et tendance corrigées", color='g')
    plt.xlabel("Temps (Année-Mois)")
    plt.ylabel("Hauteur des vagues (m)")
    plt.title("Variation de la Hauteur des Vagues après Correction de la Saison (2000 - 2023)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    # Sauvegarder le graphique sous forme de fichier PNG
    plot_filename = "/home/mauger/Projects/example-app/wave_height_detrended.png"
    plt.savefig(plot_filename)
    print(f"Graphique saisonnalité corrigée sauvegardé sous {plot_filename}")

    # Facultatif : fermer le graphique pour libérer des ressources
    plt.close()

else:
    print(f"Erreur : {output_file} n'existe pas.")
    
    # Check if file exists
if os.path.exists(output_file):
    # Load dataset
    ds = xr.open_dataset(output_file)
    
    # Extract wave height (VHM0) and time
    wave_heights = ds["VHM0"].values
    time = ds["time"].values

    # Compute mean wave height over spatial dimensions if needed
    wave_heights_mean = wave_heights.mean(axis=(1, 2))  

    # Convert time to pandas datetime
    time_dt = pd.to_datetime(time)

    # Create DataFrame
    df = pd.DataFrame({"Time": time_dt, "Mean_Wave_Height": wave_heights_mean})
    df.set_index("Time", inplace=True)

    # Compute yearly mean wave height
    df_yearly = df.resample('Y').mean()

    # Convert to NumPy array
    yearly_means = df_yearly["Mean_Wave_Height"].values
    years = df_yearly.index.year.values

    # Print results
    print("Yearly Mean Wave Heights:", yearly_means)

    # Plot the trend
    plt.figure(figsize=(10, 5))
    plt.plot(years, yearly_means, marker="o", linestyle="-", color="b", label="Yearly Mean Wave Height")
    plt.xlabel("Year")
    plt.ylabel("Mean Wave Height (m)")
    plt.title("Yearly Mean Wave Height Trend")
    plt.legend()
    plt.grid(True)
    plt.savefig("yearly_wave_height_trend.png", dpi=300)
    print("Plot saved as yearly_wave_height_trend.png")


else:
    print(f"Error: {output_file} not found")