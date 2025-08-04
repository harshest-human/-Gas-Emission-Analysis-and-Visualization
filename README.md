# Gas Concentration and Emission Analysis

A Python-based system for calculating greenhouse gas emissions from livestock facilities using CO₂-based ventilation rate measurements.

## Overview

This project processes sensor data from livestock barns to calculate:
- Ventilation rates using CO₂ mass balance
- Gas concentration differences (NH₃, CH₄, CO₂)
- Emission rates (g/h) for environmental monitoring and compliance

## Features

- **Custom CSV Parser**: Handles malformed CSV files with quote formatting issues
- **Environmental Corrections**: Accounts for temperature and time-of-day variations
- **Animal Physiology**: Calculates heat production based on body weight, milk production, and pregnancy
- **Dual-Side Analysis**: Separate calculations for North and South barn sections
- **Multiple Gas Types**: Supports NH₃, CH₄, and CO₂ emission calculations

## Requirements

```python
pandas>=1.3.0
numpy>=1.20.0
```

## Installation

1. Clone or download the project files
2. Install required packages:
```bash
pip install pandas numpy
```

## Input Data Format

### Required CSV Columns:
- `DATE.TIME`: Timestamp (YYYY-MM-DD HH:MM:SS)
- `Temperature`: Ambient temperature (°C)
- `m_weight`: Average animal body weight (kg)
- `Y1_milk_prod`: Milk production rate (kg/day)
- `p_pregnancy_day`: Days since conception
- `n_animals`: Number of animals in facility
- `CO2_in`, `CO2_N`, `CO2_S`: CO₂ concentrations (ppm) - inlet, North outlet, South outlet
- `CH4_in`, `CH4_N`, `CH4_S`: CH₄ concentrations (ppm) - inlet, North outlet, South outlet
- `NH3_in`, `NH3_N`, `NH3_S`: NH₃ concentrations (ppm) - inlet, North outlet, South outlet

### Example Data Structure:
```csv
DATE.TIME,Temperature,m_weight,Y1_milk_prod,p_pregnancy_day,n_animals,CO2_in,CO2_N,CO2_S,CH4_in,CH4_N,CH4_S,NH3_in,NH3_N,NH3_S
2025-04-08 12:00:00,18.21,545.18,30.06,119.55,42.5,522.47,415.9,419.4,13.87,3.0,3.5,1.27,0.7,0.7
```

## Usage

### Basic Usage:
```python
python simple_gas_analysis.py
```

### File Configuration:
The script expects:
- **Input file**: `gas_analysis.csv` (your sensor data)
- **Output file**: `20250408-15_ringversuche_emission_combined_data.csv` (results)

### Programmatic Usage:
```python
import pandas as pd
from simple_gas_analysis import compute_emission_and_deltas, clean_csv_data

# Load and clean data
df = clean_csv_data("your_data.csv")

# Calculate emissions
results = compute_emission_and_deltas(df)

# Save results
results.to_csv("output.csv", index=False)
```

## Output Data

The script generates a CSV file with all original data plus calculated values:

### Calculated Columns:
- `A_corr`: Temperature/time correction factor
- `Phi_tot`: Total animal heat production (W)
- `Phi_T_corr`: Temperature-corrected heat production
- `P_CO2_T_A_all_animal`: Total CO₂ production (kg/h)
- `Q_Vent_rate_N`, `Q_Vent_rate_S`: Ventilation rates (m³/h)

For each gas (NH₃, CH₄, CO₂) and side (N, S):
- `delta_{gas}_{side}_ppm`: Concentration difference (ppm)
- `delta_{gas}_{side}_mgm3`: Mass concentration difference (mg/m³)
- `e_{gas}_{side}`: Emission rate (g/h)

## Scientific Background

### Ventilation Rate Calculation:
Uses CO₂ mass balance principle:
```
Ventilation Rate = CO₂ Production / (CO₂_inlet - CO₂_outlet)
```

### Animal Heat Production:
Based on metabolic scaling laws:
```
Heat = 5.6 × (body_weight^0.75) + 22 × milk_production + 1.6×10⁻⁵ × (pregnancy_days³)
```

### Emission Calculation:
```
Emission = (Concentration_difference × Ventilation_rate) / 1000
```

## Constants Used

- **P_CO2_term**: 0.185 (CO₂ production factor)
- **Temperature correction**: Accounts for ambient temperature effects
- **Circadian correction**: Daily activity pattern adjustment
- **Molecular masses**: CO₂ (44.01), NH₃ (17.031), CH₄ (16.04) g/mol

