from pathlib import Path
import numpy as np
import os
import matplotlib.pyplot as plt
import yaml
from envi2 import *  # Ensure you have the required `envi2` file
from matplotlib.patches import Rectangle

def process_folder(folder_path):
    """
    Processes a folder containing .hdr and .dat files to extract average reflectance spectra.
    Returns a list of spectra and the wavelengths.
    """
    all_spectra = []
    wavelengths = None

    for file in sorted(os.listdir(folder_path)):
        if file.endswith('.hdr'):
            print(f"Processing: {file}")
            header_file_path = Path(folder_path) / file
            reflectance_image, wavelengths, header = read_envi(header_file=header_file_path, normalize=False)

            # Define the region of interest (ROI)
            x_end = reflectance_image.shape[1] - 50
            y_end = reflectance_image.shape[0] - 50

            # Compute the average reflectance spectrum for the ROI
            reflectance_spectrum = np.mean(reflectance_image[50:y_end, 50:x_end, :], axis=(0, 1))
            all_spectra.append(reflectance_spectrum)

    return np.array(all_spectra), wavelengths

def standardize_spectra(spectra):
    """
    Standardizes each spectrum to have mean=0 and std=1.
    """
    return (spectra - np.mean(spectra, axis=1, keepdims=True)) / np.std(spectra, axis=1, keepdims=True)

def compute_first_derivative(spectra, wavelengths):
    """
    Computes the first derivative of reflectance spectra with respect to wavelengths.
    """
    return np.gradient(spectra, wavelengths, axis=1)

def compute_second_derivative(spectra, wavelengths):
    """
    Computes the second derivative of reflectance spectra with respect to wavelengths.
    """
    first_derivative = compute_first_derivative(spectra, wavelengths)
    return np.gradient(first_derivative, wavelengths, axis=1)

def plot_spectra(folders, transformation, is_ref):
    """
    Plots spectra based on the specified transformation and flag for 'ref' or 'charring'.
    """
    colors = ['blue', 'green', 'red', 'orange']  # Colors for each class
    plt.figure(figsize=(12, 8))

    # Process each folder
    for i, folder in enumerate(folders):
        spectra, wavelengths = process_folder(folder)

        # Apply transformation
        if transformation == "SNV":
            transformed_spectra = standardize_spectra(spectra)
        elif transformation == "first_derivative":
            transformed_spectra = compute_first_derivative(spectra, wavelengths)
        elif transformation == "second_derivative":
            transformed_spectra = compute_second_derivative(spectra, wavelengths)
        else:
            transformed_spectra = spectra

        mean_spectrum = np.mean(transformed_spectra, axis=0)
        std_spectrum = np.std(transformed_spectra, axis=0)

        # Plot spectra
        plt.plot(wavelengths, mean_spectrum, label=f'Level {i}', color=colors[i])
        plt.fill_between(wavelengths, mean_spectrum - std_spectrum, mean_spectrum + std_spectrum, 
                         color=colors[i], alpha=0.2)

    # Add vertical lines and shaded regions based on the flag
    if is_ref:
        plt.axvline(x=1700, color='blue', linestyle='--', linewidth=1.5)
        plt.axvline(x=1750, color='blue', linestyle='--', linewidth=1.5)
        plt.axvline(x=2300, color='black', linestyle='--', linewidth=1.5)
        plt.axvline(x=2350, color='black', linestyle='--', linewidth=1.5)
        plt.axvspan(1700, 1750, color='lightblue', alpha=0.3)
        plt.axvspan(2300, 2350, color='lightgray', alpha=0.3)
    else:  # Charring
        plt.axvline(x=1300, color='blue', linestyle='--', linewidth=1.5)
        plt.axvline(x=1400, color='blue', linestyle='--', linewidth=1.5)
        plt.axvline(x=1850, color='magenta', linestyle='--', linewidth=1.5)
        plt.axvline(x=1900, color='magenta', linestyle='--', linewidth=1.5)
        plt.axvline(x=2250, color='black', linestyle='--', linewidth=1.5)
        plt.axvline(x=2350, color='black', linestyle='--', linewidth=1.5)
        plt.axvspan(1300, 1400, color='lightblue', alpha=0.3)
        plt.axvspan(1850, 1900, color='magenta', alpha=0.3)
        plt.axvspan(2250, 2350, color='lightgray', alpha=0.3)

    # Configure plot
    plt.xlabel('Wavelength (nm)', fontsize=24)
    ylabel = 'Reflectance'
    if transformation == "SNV":
        ylabel = 'Standardized Reflectance'
    elif transformation == "first_derivative":
        ylabel = 'First Derivative of Reflectance'
    elif transformation == "second_derivative":
        ylabel = 'Second Derivative of Reflectance'
    plt.ylabel(ylabel, fontsize=24)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.legend(fontsize=24)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Load configuration from YAML
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

folders = config['folders']
transformation = config['transformation']
is_ref = config['is_ref']

# Plot spectra
plot_spectra(folders, transformation, is_ref)
