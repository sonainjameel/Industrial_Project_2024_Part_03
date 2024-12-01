
# Industrial Project Part 3: Reflectance Analysis and Spectral Transformations 

> **_⚠️ Note:_**  
> **_This code has been tested on Python versions 3.10.5 and 3.12.4._** 

This project processes and analyzes reflectance spectra from spectral data. It provides transformation options (e.g., SNV, first derivative, second derivative) and dynamically adjusts visualization for either `Ref` or `Charring` analysis based on the input configuration.

## Features

- **Spectral Analysis**: Processes reflectance data from specified folders.
- **Transformation Options**:
  - No Transformation
  - Standard Normal Variate (SNV)
  - First Derivative
  - Second Derivative
- **Custom Visualization**: Automatically adjusts shaded regions and vertical lines for `Ref` or `Charring` levels.
- **Configurable Parameters**: Uses a `config.yaml` file to specify input folders, transformation type, and analysis type.

## Installation

### Requirements

- Python 3.8 or higher
- The following Python libraries:
  - `numpy`
  - `matplotlib`
  - `PyYAML`

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sonainjameel/Industrial_Project_2024_Part_03.git
   cd Industrial_Project_2024_Part_03
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Input Data**: Ensure your `.hdr` and `.raw` files are placed in the folders specified in `config.yaml`.

## Configuration

The project relies on a `config.yaml` file to specify input paths, transformation type, and whether the analysis is for `Ref` or `Charring`. Below is an example configuration:

```yaml
folders:
  - "path/to/folder1"  # Folder for Oil Level 0 data
  - "path/to/folder2"  # Folder for Oil Level 1 data
  - "path/to/folder3"  # Folder for Oil Level 2 data
  - "path/to/folder4"  # Folder for Oil Level 3 data
transformation: "first_derivative"  # Options: "no", "SNV", "first_derivative", "second_derivative"
is_ref: true  # true for 'Ref' analysis, false for 'Charring' analysis
```

## Usage

To process the spectra and generate the plots, run the `spectral_analysis.py` script with the `config.yaml` file as input:

```bash
python3 spectral_analysis.py config.yaml
```

### Example Outputs

- **Ref Analysis (First Derivative)**:
  - Shaded regions: Light blue (1700–1750 nm), Light gray (2300–2350 nm)
  - Reflectance transformed using the no transformation

- **Charring Analysis (SNV)**:
  - Shaded regions: Light blue (1300–1400 nm), Magenta (1850–1900 nm), Light gray (2250-2350 nm)
  - Reflectance normalized using SNV

## Project Structure

```
Industrial_Project_2024_Part_03/
├── config.yaml               # Configuration file for paths and parameters
├── spectral_analysis.py      # Script for spectral processing and plotting
├── requirements.txt          # Required libraries
```

## Available Transformations

- **None**: Uses raw reflectance spectra without any modification.
- **SNV (Standard Normal Variate)**: Normalizes each spectrum to mean 0 and standard deviation 1.
- **First Derivative**: Highlights spectral changes using the first derivative.
- **Second Derivative**: Emphasizes rapid spectral changes using the second derivative.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with a clear message.
4. Submit a pull request for review.

## License

This project is licensed under the MIT License.

## Acknowledgements

Special thanks to Sonain, Kasem, and Turab for their efforts, and to Joni Hyttinen and Prof. Markku Keinänen for their guidance and support throughout the project.
