"""
01_process_spectra.py

Purpose:
Process Spectral Evolution .sed files collected for the
intertidal spectral-taxonomic diversity project.

Workflow adapted from Cabrera's original SED.py and Normalize.py:
1. Read target radiance from .sed files.
2. Restrict spectra to 400-900 nm.
3. Average five Spectralon white-reference measurements.
4. Convert target radiance to relative reflectance.
5. Preserve individual target measurements for subsequent
   quadrat assignment and spectral-diversity analysis.

IMPORTANT:
Do not average the three within-quadrat spectral replicates here.
"""

import os
import pandas as pd

""" FUNCTIONS """
def read_sed_file(filepath, use_column=2):
    metadata = {}
    wavelengths = []
    radiances = []

    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Extract metadata
    for line in lines:
        if line.startswith('Latitude:'):
            val = line.split(':')[1].strip()
            metadata['latitude'] = float(val) if val.lower() != 'n/a' else None
        elif line.startswith('Longitude:'):
            val = line.split(':')[1].strip()
            metadata['longitude'] = float(val) if val.lower() != 'n/a' else None
        elif line.startswith('GPS Time:'):
            metadata['gps_time'] = line.split(':', 1)[1].strip()
        elif line.strip().startswith('Data:'):
            data_start_idx = lines.index(line) + 2
            break
    else:
        raise ValueError(f"No 'Data:' section found in {filepath}")

    for line in lines[data_start_idx:]:
        if line.strip():
            parts = line.strip().split()
            if len(parts) > use_column:
                try:
                    wavelengths.append(float(parts[0]))
                    radiances.append(float(parts[use_column]))
                except ValueError:
                    continue

    return metadata, wavelengths, radiances

def process_sed_directory(directory, output_dir=None, use_column=2):
    sed_files = sorted(
        [f for f in os.listdir(directory)
         if f.lower().endswith('.sed')]
    )

    if not sed_files:
        raise ValueError(f"No .sed files found in {directory}.")

    spectra_dict = {}
    wavelengths_master = None
    meta_records = []

    for filename in sed_files:
        filepath = os.path.join(directory, filename)
        metadata, wavelengths, radiances = read_sed_file(filepath, use_column=use_column)
        basename = os.path.splitext(filename)[0]

        if wavelengths_master is None:
            wavelengths_master = wavelengths
        elif wavelengths != wavelengths_master:
            raise ValueError(f"Wavelength mismatch in file: {filename}")

        spectra_dict[basename] = radiances

        meta_records.append({
            'filename': basename,
            'latitude': metadata.get('latitude'),
            'longitude': metadata.get('longitude'),
            'gps_time': metadata.get('gps_time')
        })

    df = pd.DataFrame(spectra_dict, index=wavelengths_master)
    df.index.name = 'wavelength'
    meta_df = pd.DataFrame(meta_records)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(os.path.join(output_dir, 'LCDM_050225_radiance.csv'))
        meta_df.to_csv(os.path.join(output_dir, 'LCDM_050225_radiance_metadata.csv'), index=False)

    return df, meta_df


""" Normalize Spectra """

def calculate_relative_reflectance(spectra_df, reference_df):

    # Restrict sample spectra to 400-900 nm
    target_spectra = spectra_df.loc[400:900]

    # Restrict Spectralon reference spectra to 400-900 nm
    reference_spectra = reference_df.loc[400:900]

    # Average the five Spectralon measurements at each wavelength
    white_reference = reference_spectra.mean(axis=1)

    # Divide each sample spectrum by the mean Spectralon spectrum
    relative_reflectance = target_spectra.div(
        white_reference,
        axis=0
    )

    return relative_reflectance, white_reference

""" RUN PROCESSING """

# Folder containing sample .sed files
directory = r"C:\Users\Gabriela Shirkey\OneDrive - Chapman University\CONNECT_SBG\Coastal-Tanner\SpectralEvolution\LCDM_2005_3A02\LCDM 05_02"

# Folder containing the five Spectralon .sed files
reference_dir = r"C:\Users\Gabriela Shirkey\OneDrive - Chapman University\CONNECT_SBG\Coastal-Tanner\SpectralEvolution\LCDM_2005_3A02\LCDM 05_02\Reference"

# Folder for processed outputs
output_dir = r"C:\Users\Gabriela Shirkey\OneDrive - Chapman University\CONNECT_SBG\Coastal-Tanner\SpectralEvolution\LCDM_2005_3A02\LCDM_2005_3A02_processed"


# Read sample .sed files
spectra_df, metadata_df = process_sed_directory(
    directory,
    output_dir
)


# Read the five Spectralon reference .sed files
reference_df, reference_metadata_df = process_sed_directory(
    reference_dir
)

# Confirm that exactly five Spectralon measurements were read
if reference_df.shape[1] != 5:
    raise ValueError(
        f"Expected 5 Spectralon reference spectra, "
        f"but found {reference_df.shape[1]}."
    )

# Calculate relative reflectance
relative_reflectance, white_reference = calculate_relative_reflectance(
    spectra_df,
    reference_df
)

# Save relative reflectance
relative_reflectance.to_csv(
    os.path.join(
        output_dir,
        "LCDM_050225_relative_reflectance.csv"
    )
)

# Save the mean Spectralon white reference
white_reference.to_csv(
    os.path.join(
        output_dir,
        "LCDM_050225_white_reference.csv"
    ),
    header=["mean_spectralon"]
)

## sample plots after quadrat identities have been assigned
close_quadrats = quadrat_table[quadrat_table["distance_m"] <= 10].sample(5)
mid_quadrats = quadrat_table[
    quadrat_table["distance_m"].between(20, 30)
].sample(5)
far_quadrats = quadrat_table[quadrat_table["distance_m"] >= 40].sample(5)

qc_quadrats = pd.concat([
    close_quadrats,
    mid_quadrats,
    far_quadrats
])