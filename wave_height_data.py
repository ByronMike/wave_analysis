import copernicusmarine
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

# Define the absolute file path where the data will be saved
output_file = "/home/mauger/Projects/example-app/wave_height_data.nc"

# Download the wave height data (VHM0) and save it as a NetCDF file
response = copernicusmarine.subset(
    dataset_id="med-hcmr-wav-rean-h",
    variables=["VHM0"],  # Significant wave height
    minimum_longitude=4.564384588158627,
    maximum_longitude=5.132210688383661,
    minimum_latitude=42.673261612601905,
    maximum_latitude=43.24108771282694,
    start_datetime="2000-01-01T23:00:00",
    end_datetime="2023-01-01T23:00:00",
    output_filename=output_file,  # Save the data to a file
)

# Check the response for success or failure
print(response)

