import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

def load_emission_data(filename):
    """Load the processed emission data"""
    df = pd.read_csv(filename)
    df['DATE.TIME'] = pd.to_datetime(df['DATE.TIME'])
    return df

def plot_emission_overview(df):
    """Create overview plots of all gas emissions"""
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    fig.suptitle('Gas Emission Analysis Overview', fontsize=16, fontweight='bold')
    
    gases = ['NH3', 'CH4', 'CO2']
    colors = ['red', 'blue', 'green']
    
    for i, gas in enumerate(gases):
        # North side emissions
        axes[i, 0].plot(df['DATE.TIME'], df[f'e_{gas}_N'], 
                       color=colors[i], linewidth=2, label=f'{gas} North')
        axes[i, 0].set_title(f'{gas} Emissions - North Side')
        axes[i, 0].set_ylabel('Emission Rate (g/h)')
        axes[i, 0].grid(True, alpha=0.3)
        axes[i, 0].tick_params(axis='x', rotation=45)
        
        # South side emissions
        axes[i, 1].plot(df['DATE.TIME'], df[f'e_{gas}_S'], 
                       color=colors[i], linewidth=2, label=f'{gas} South')
        axes[i, 1].set_title(f'{gas} Emissions - South Side')
        axes[i, 1].set_ylabel('Emission Rate (g/h)')
        axes[i, 1].grid(True, alpha=0.3)
        axes[i, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('emission_overview.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_ventilation_rates(df):
    """Plot ventilation rates for both sides"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle('Ventilation Rates Analysis', fontsize=16, fontweight='bold')
    
    # Time series plot
    ax1.plot(df['DATE.TIME'], df['Q_Vent_rate_N'], 
             color='blue', linewidth=2, label='North Side', alpha=0.7)
    ax1.plot(df['DATE.TIME'], df['Q_Vent_rate_S'], 
             color='red', linewidth=2, label='South Side', alpha=0.7)
    ax1.set_title('Ventilation Rates Over Time')
    ax1.set_ylabel('Ventilation Rate (m³/h)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Comparison boxplot
    vent_data = pd.DataFrame({
        'North': df['Q_Vent_rate_N'],
        'South': df['Q_Vent_rate_S']
    })
    vent_data.boxplot(ax=ax2)
    ax2.set_title('Ventilation Rate Distribution Comparison')
    ax2.set_ylabel('Ventilation Rate (m³/h)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ventilation_rates.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_concentration_differences(df):
    """Plot gas concentration differences"""
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle('Gas Concentration Differences (Inlet - Outlet)', fontsize=16, fontweight='bold')
    
    gases = ['NH3', 'CH4', 'CO2']
    colors = ['red', 'blue', 'green']
    
    for i, gas in enumerate(gases):
        axes[i].plot(df['DATE.TIME'], df[f'delta_{gas}_N_ppm'], 
                    color=colors[i], linewidth=2, label=f'{gas} North', alpha=0.7)
        axes[i].plot(df['DATE.TIME'], df[f'delta_{gas}_S_ppm'], 
                    color=colors[i], linewidth=2, linestyle='--', label=f'{gas} South', alpha=0.7)
        axes[i].set_title(f'{gas} Concentration Difference')
        axes[i].set_ylabel('Δ Concentration (ppm)')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
        axes[i].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('concentration_differences.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_daily_patterns(df):
    """Plot daily emission patterns"""
    df['hour'] = df['DATE.TIME'].dt.hour
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Daily Emission Patterns', fontsize=16, fontweight='bold')
    
    # Group data by hour for average patterns
    hourly_avg = df.groupby('hour').agg({
        'e_NH3_N': 'mean', 'e_NH3_S': 'mean',
        'e_CH4_N': 'mean', 'e_CH4_S': 'mean',
        'e_CO2_N': 'mean', 'e_CO2_S': 'mean',
        'Temperature': 'mean'
    }).reset_index()
    
    # NH3 daily pattern
    axes[0, 0].plot(hourly_avg['hour'], hourly_avg['e_NH3_N'], 
                   'ro-', label='North', linewidth=2)
    axes[0, 0].plot(hourly_avg['hour'], hourly_avg['e_NH3_S'], 
                   'bo-', label='South', linewidth=2)
    axes[0, 0].set_title('NH₃ Daily Pattern')
    axes[0, 0].set_ylabel('Avg Emission (g/h)')
    axes[0, 0].set_xlabel('Hour of Day')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # CH4 daily pattern
    axes[0, 1].plot(hourly_avg['hour'], hourly_avg['e_CH4_N'], 
                   'go-', label='North', linewidth=2)
    axes[0, 1].plot(hourly_avg['hour'], hourly_avg['e_CH4_S'], 
                   'mo-', label='South', linewidth=2)
    axes[0, 1].set_title('CH₄ Daily Pattern')
    axes[0, 1].set_ylabel('Avg Emission (g/h)')
    axes[0, 1].set_xlabel('Hour of Day')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # CO2 daily pattern
    axes[1, 0].plot(hourly_avg['hour'], hourly_avg['e_CO2_N'], 
                   'co-', label='North', linewidth=2)
    axes[1, 0].plot(hourly_avg['hour'], hourly_avg['e_CO2_S'], 
                   'yo-', label='South', linewidth=2)
    axes[1, 0].set_title('CO₂ Daily Pattern')
    axes[1, 0].set_ylabel('Avg Emission (g/h)')
    axes[1, 0].set_xlabel('Hour of Day')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Temperature pattern
    axes[1, 1].plot(hourly_avg['hour'], hourly_avg['Temperature'], 
                   'ko-', linewidth=2)
    axes[1, 1].set_title('Temperature Daily Pattern')
    axes[1, 1].set_ylabel('Temperature (°C)')
    axes[1, 1].set_xlabel('Hour of Day')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('daily_patterns.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_correlation_heatmap(df):
    """Create correlation heatmap of key variables"""
    # Select key variables for correlation analysis
    correlation_vars = [
        'Temperature', 'n_animals', 'm_weight', 'Y1_milk_prod',
        'Q_Vent_rate_N', 'Q_Vent_rate_S',
        'e_NH3_N', 'e_NH3_S', 'e_CH4_N', 'e_CH4_S', 'e_CO2_N', 'e_CO2_S'
    ]
    
    corr_data = df[correlation_vars].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_data, annot=True, cmap='RdBu_r', center=0, 
                fmt='.2f', square=True, cbar_kws={'label': 'Correlation Coefficient'})
    plt.title('Correlation Matrix: Environmental and Emission Variables', 
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_emission_summary_stats(df):
    """Create summary statistics plots"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Emission Summary Statistics', fontsize=16, fontweight='bold')
    
    # Total emissions by gas type
    gas_totals = {
        'NH₃': df['e_NH3_N'].sum() + df['e_NH3_S'].sum(),
        'CH₄': df['e_CH4_N'].sum() + df['e_CH4_S'].sum(),
        'CO₂': df['e_CO2_N'].sum() + df['e_CO2_S'].sum()
    }
    
    axes[0, 0].bar(gas_totals.keys(), gas_totals.values(), 
                  color=['red', 'blue', 'green'], alpha=0.7)
    axes[0, 0].set_title('Total Emissions by Gas Type')
    axes[0, 0].set_ylabel('Total Emission (g)')
    
    # North vs South comparison
    sides_data = {
        'North': df['e_NH3_N'].sum() + df['e_CH4_N'].sum() + df['e_CO2_N'].sum(),
        'South': df['e_NH3_S'].sum() + df['e_CH4_S'].sum() + df['e_CO2_S'].sum()
    }
    
    axes[0, 1].bar(sides_data.keys(), sides_data.values(), 
                  color=['blue', 'red'], alpha=0.7)
    axes[0, 1].set_title('Total Emissions: North vs South')
    axes[0, 1].set_ylabel('Total Emission (g)')
    
    # Average hourly emissions
    avg_emissions = [
        df['e_NH3_N'].mean() + df['e_NH3_S'].mean(),
        df['e_CH4_N'].mean() + df['e_CH4_S'].mean(),
        df['e_CO2_N'].mean() + df['e_CO2_S'].mean()
    ]
    
    axes[1, 0].bar(['NH₃', 'CH₄', 'CO₂'], avg_emissions, 
                  color=['red', 'blue', 'green'], alpha=0.7)
    axes[1, 0].set_title('Average Hourly Emissions')
    axes[1, 0].set_ylabel('Avg Emission Rate (g/h)')
    
    # Emission rate distribution
    all_emissions = np.concatenate([
        df['e_NH3_N'], df['e_NH3_S'], df['e_CH4_N'], 
        df['e_CH4_S'], df['e_CO2_N'], df['e_CO2_S']
    ])
    
    axes[1, 1].hist(all_emissions, bins=30, alpha=0.7, color='purple')
    axes[1, 1].set_title('Distribution of All Emission Rates')
    axes[1, 1].set_xlabel('Emission Rate (g/h)')
    axes[1, 1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('emission_summary.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_all_plots(data_file):
    """Generate all visualization plots"""
    print("📊 Loading emission data...")
    df = load_emission_data(data_file)
    
    print("🎨 Generating emission overview plots...")
    plot_emission_overview(df)
    
    print("🌬️ Generating ventilation rate plots...")
    plot_ventilation_rates(df)
    
    print("📈 Generating concentration difference plots...")
    plot_concentration_differences(df)
    
    print("🕐 Generating daily pattern analysis...")
    plot_daily_patterns(df)
    
    print("🔗 Generating correlation heatmap...")
    plot_correlation_heatmap(df)
    
    print("📋 Generating summary statistics...")
    plot_emission_summary_stats(df)
    
    print("✅ All plots generated and saved!")
    print("\nGenerated files:")
    print("- emission_overview.png")
    print("- ventilation_rates.png") 
    print("- concentration_differences.png")
    print("- daily_patterns.png")
    print("- correlation_heatmap.png")
    print("- emission_summary.png")

if __name__ == "__main__":
    # Set up plotting style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # File containing the emission analysis results
    data_file = "20250408-15_ringversuche_emission_combined_data.csv"
    
    try:
        generate_all_plots(data_file)
    except FileNotFoundError:
        print(f"❌ File not found: {data_file}")
        print("Please run the emission analysis first to generate the data file.")
    except Exception as e:
        print(f"❌ Error generating plots: {str(e)}")
