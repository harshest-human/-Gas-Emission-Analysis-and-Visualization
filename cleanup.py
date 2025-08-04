#!/usr/bin/env python3
"""
Cleanup Script for Gas Emission Analysis
Removes generated files and temporary folders
"""

import os
import glob
import shutil
import sys

def cleanup_all_files():
    """Remove all generated files including processed data"""
    print("🧹 FULL CLEANUP: Removing ALL generated files...")
    
    # Plot files
    plot_files = [
        "emission_overview.png",
        "ventilation_rates.png", 
        "concentration_differences.png",
        "daily_patterns.png",
        "correlation_heatmap.png",
        "emission_summary.png"
    ]
    
    # Data files
    data_files = [
        "20250408-15_ringversuche_emission_combined_data.csv"
    ]
    
    # All files to remove
    all_files = plot_files + data_files
    
    deleted_count = 0
    
    # Remove specific files
    for file in all_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✓ Deleted: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"✗ Error deleting {file}: {e}")
    
    # Remove any additional PNG files
    png_files = glob.glob("*.png")
    for file in png_files:
        if file not in plot_files:  # Avoid double-counting
            try:
                os.remove(file)
                print(f"✓ Deleted: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"✗ Error deleting {file}: {e}")
    
    # Remove temporary folders
    temp_folders = ["__pycache__", ".ipynb_checkpoints"]
    for folder in temp_folders:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"✓ Deleted folder: {folder}")
                deleted_count += 1
            except Exception as e:
                print(f"✗ Error deleting folder {folder}: {e}")
    
    print(f"\n🎉 Cleanup complete! Removed {deleted_count} items.")
    return deleted_count

def cleanup_plots_only():
    """Remove only plot files, keep processed data"""
    print("🎨 PLOTS CLEANUP: Removing only visualization files...")
    
    plot_files = [
        "emission_overview.png",
        "ventilation_rates.png", 
        "concentration_differences.png",
        "daily_patterns.png",
        "correlation_heatmap.png",
        "emission_summary.png"
    ]
    
    deleted_count = 0
    
    # Remove plot files
    for file in plot_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✓ Deleted: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"✗ Error deleting {file}: {e}")
    
    # Remove any additional PNG files
    png_files = glob.glob("*.png")
    for file in png_files:
        if file not in plot_files:  # Catch any missed PNG files
            try:
                os.remove(file)
                print(f"✓ Deleted: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"✗ Error deleting {file}: {e}")
    
    print(f"\n🎉 Plot cleanup complete! Removed {deleted_count} items.")
    return deleted_count

def show_menu():
    """Display cleanup options"""
    print("\n" + "="*50)
    print("🧹 GAS EMISSION ANALYSIS - CLEANUP TOOL")
    print("="*50)
    print("1. Clean plots only (keep processed data)")
    print("2. Clean everything (plots + processed data)")  
    print("3. Show current files")
    print("4. Exit")
    print("-"*50)
    
def show_current_files():
    """Show what files currently exist"""
    print("\n📁 Current generated files:")
    
    # Check for plot files
    plot_files = [
        "emission_overview.png",
        "ventilation_rates.png", 
        "concentration_differences.png",
        "daily_patterns.png",
        "correlation_heatmap.png",
        "emission_summary.png"
    ]
    
    print("\n🎨 Plot files:")
    plot_count = 0
    for file in plot_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024  # KB
            print(f"  ✓ {file} ({size:.1f} KB)")
            plot_count += 1
        else:
            print(f"  ✗ {file} (not found)")
    
    # Check for data files
    data_files = ["20250408-15_ringversuche_emission_combined_data.csv"]
    print("\n📊 Data files:")
    data_count = 0
    for file in data_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024  # KB
            print(f"  ✓ {file} ({size:.1f} KB)")
            data_count += 1
        else:
            print(f"  ✗ {file} (not found)")
    
    # Check for other PNG files
    other_pngs = [f for f in glob.glob("*.png") if f not in plot_files]
    if other_pngs:
        print("\n🖼️ Other PNG files:")
        for file in other_pngs:
            size = os.path.getsize(file) / 1024  # KB
            print(f"  ✓ {file} ({size:.1f} KB)")
    
    # Check for temp folders
    temp_folders = ["__pycache__", ".ipynb_checkpoints"]
    temp_count = 0
    for folder in temp_folders:
        if os.path.exists(folder):
            print(f"  📁 {folder}/ (temp folder)")
            temp_count += 1
    
    total_files = plot_count + data_count + len(other_pngs) + temp_count
    print(f"\n📈 Total: {total_files} items")

def main():
    """Main cleanup interface"""
    if len(sys.argv) > 1:
        # Command line argument
        arg = sys.argv[1].lower()
        if arg in ['all', 'everything', 'full']:
            cleanup_all_files()
        elif arg in ['plots', 'png', 'images']:
            cleanup_plots_only()
        elif arg in ['show', 'list', 'status']:
            show_current_files()
        else:
            print("Usage: python cleanup.py [all|plots|show]")
    else:
        # Interactive mode
        while True:
            show_menu()
            choice = input("Choose an option (1-4): ").strip()
            
            if choice == '1':
                cleanup_plots_only()
                break
            elif choice == '2':
                cleanup_all_files()
                break
            elif choice == '3':
                show_current_files()
            elif choice == '4':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
