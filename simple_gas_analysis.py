import pandas as pd
import numpy as np
import os
import glob

def compute_emission_and_deltas(df):
    """
    Compute CO₂-based ventilation rates, gas concentration deltas (ppm and mg/m³),
    and emissions (g/h) for NH₃, CH₄, and CO₂ in both North and South directions.

    Required DataFrame columns:
    - DATE.TIME, Temperature, m_weight, Y1_milk_prod, p_pregnancy_day, n_animals
    - CO2_in, CO2_N, CO2_S, CH4_in, CH4_N, CH4_S, NH3_in, NH3_N, NH3_S
    """
    constants = {
        "P_CO2_term": 0.185,
        "a": 0.22,
        "h_min": 2.9,
        "CO2_Molmass": 44.01,
        "NH3_Molmass": 17.031,
        "CH4_Molmass": 16.04,
        "R": 8.314472,
        "p_ref": 1013
    }

    # Ensure DATE.TIME is datetime
    df['DATE.TIME'] = pd.to_datetime(df['DATE.TIME'])
    df['hour'] = df['DATE.TIME'].dt.hour

    # A_corr: temperature correction factor
    df['A_corr'] = 1 - constants['a'] * 3 * np.sin((2 * np.pi / 24) * (df['hour'] + 6 - constants['h_min']))

    # Animal respiration heat output
    df['Phi_tot'] = 5.6 * (df['m_weight'] ** 0.75) + 22 * df['Y1_milk_prod'] + 1.6e-5 * (df['p_pregnancy_day'] ** 3)
    df['Phi_T_corr'] = df['Phi_tot'] * (1 + 4e-5 * (20 - df['Temperature']) ** 3)
    df['hpu_T_A_corr_all_animal'] = ((df['Phi_T_corr'] / 1000) * df['A_corr']) * df['n_animals']
    df['P_CO2_T_A_all_animal'] = df['hpu_T_A_corr_all_animal'] * constants['P_CO2_term']

    # Ventilation rate for North and South
    df['Q_Vent_rate_N'] = df['P_CO2_T_A_all_animal'] / ((df['CO2_in'] - df['CO2_N']) * 1e-6)
    df['Q_Vent_rate_S'] = df['P_CO2_T_A_all_animal'] / ((df['CO2_in'] - df['CO2_S']) * 1e-6)

    gases = ['NH3', 'CH4', 'CO2']
    for gas in gases:
        molmass = constants[f"{gas}_Molmass"]
        for side in ['N', 'S']:
            col_in = f"{gas}_in"
            col_out = f"{gas}_{side}"
            delta_ppm = f"delta_{gas}_{side}_ppm"
            delta_mgm3 = f"delta_{gas}_{side}_mgm3"
            emission = f"e_{gas}_{side}"

            df[delta_ppm] = df[col_in] - df[col_out]
            df[delta_mgm3] = (
                0.1 * molmass * constants['p_ref'] * df[delta_ppm]
            ) / ((df["Temperature"] + 273.15) * constants['R'])
            df[emission] = (df[delta_mgm3] * df[f"Q_Vent_rate_{side}"]) / 1000  # in g/h

    return df

# --------------------------
# Example usage (main script)
# --------------------------
def clean_csv_data(filename):
    """
    Custom parser to handle the specific CSV formatting with extra quotes
    """
    import re
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines
    lines = content.strip().split('\n')
    
    cleaned_lines = []
    for line in lines:
        # Remove the outer quotes if they exist
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]
        
        # Replace double quotes around field values with nothing
        # This regex finds patterns like ,"field", and replaces with ,field,
        line = re.sub(r',""([^"]*?)""', r',\1', line)
        line = re.sub(r'^""([^"]*?)""', r'\1', line)  # Handle first field
        line = re.sub(r',""([^"]*?)""$', r',\1', line)  # Handle last field
        
        cleaned_lines.append(line)
    
    # Create a temporary cleaned CSV content
    cleaned_content = '\n'.join(cleaned_lines)
    
    # Use StringIO to create a file-like object
    from io import StringIO
    return pd.read_csv(StringIO(cleaned_content))

def cleanup_generated_files(keep_data=True):
    """
    Clean up generated files and folders
    
    Args:
        keep_data (bool): If True, keeps the processed CSV data file
    """
    print("Cleaning up generated files...")
    
    # List of generated plot files
    plot_files = [
        "emission_overview.png",
        "ventilation_rates.png", 
        "concentration_differences.png",
        "daily_patterns.png",
        "correlation_heatmap.png",
        "emission_summary.png"
    ]
    
    # Remove plot files
    deleted_count = 0
    for file in plot_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {file}: {e}")
    
    # Remove any additional PNG files
    png_files = glob.glob("*.png")
    for file in png_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {file}: {e}")
    
    # Optionally remove processed data file
    if not keep_data:
        data_file = "20250408-15_ringversuche_emission_combined_data.csv"
        if os.path.exists(data_file):
            try:
                os.remove(data_file)
                print(f"Deleted: {data_file}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {data_file}: {e}")
    
    # Clean up any temporary folders or cache
    temp_folders = ["__pycache__", ".ipynb_checkpoints"]
    for folder in temp_folders:
        if os.path.exists(folder):
            try:
                import shutil
                shutil.rmtree(folder)
                print(f"Deleted folder: {folder}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting folder {folder}: {e}")
    
    if deleted_count == 0:
        print("No files to clean up.")
    else:
        print(f"Cleanup complete! Deleted {deleted_count} items.")
    print("-" * 50)

if __name__ == "__main__":
    # Define file paths
    input_file = "gas_analysis.csv"  
    output_file = "20250408-15_ringversuche_emission_combined_data.csv"

    # Option to clean up before running (uncomment if needed)
    # cleanup_generated_files(keep_data=False)  # Set to False to delete everything
    
    try:
        # Load data with custom parser
        print("Loading and cleaning CSV data...")
        df = clean_csv_data(input_file)
        print(f" Data loaded successfully. Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")

        # Run calculations
        print("Running emission calculations...")
        result = compute_emission_and_deltas(df)

        # Save result
        result.to_csv(output_file, index=False)
        print(f"Emission results saved to: {output_file}")

    except FileNotFoundError:
        print(f" File not found: {input_file}. Please check the file path.")
    except Exception as e:
        print(f" Error processing data: {str(e)}")
        print("Check if all required columns are present in the CSV file.")
