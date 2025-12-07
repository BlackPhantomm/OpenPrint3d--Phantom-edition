import os
import json
import re

# CONFIGURATION
# ---------------------------------------------------------
MAINTAINER = "BlackPhantomm"
SCHEMA_VER = "1.0.0"
ID_PREFIX = "phantom_"

def get_input(prompt, default=None):
    """Helper to get input with an optional default value."""
    if default:
        user_in = input(f"{prompt} [{default}]: ").strip()
        return user_in if user_in else default
    else:
        while True:
            user_in = input(f"{prompt}: ").strip()
            if user_in: return user_in

def clean_id(name):
    """Turns 'Ender 3 V3 KE' into 'ender3_v3_ke'"""
    # Lowercase, replace spaces/special chars with underscores
    clean = name.lower()
    clean = re.sub(r'[^a-z0-9]+', '_', clean)
    return clean.strip('_')

def create_filament():
    print("\n--- Creating New Filament ---")
    name = get_input("Display Name (e.g. Phantom PLA+)")
    material = get_input("Material Type", "PLA")
    brand = get_input("Brand", "Generic")
    color = get_input("Color Hex Code", "0000FF")
    temp_nozzle = int(get_input("Nozzle Temp (°C)", "210"))
    temp_bed = int(get_input("Bed Temp (°C)", "60"))
    
    file_id = f"{ID_PREFIX}{clean_id(name)}"
    
    data = {
        "schema_version": SCHEMA_VER,
        "type": "filament",
        "id": file_id,
        "maintainer": MAINTAINER,
        "metadata": {
            "name": name,
            "author": MAINTAINER,
            "color": color
        },
        "compatibility": {
            "printers": ["*"],
            "nozzles": ["0.4", "0.6"]
        },
        "parameters": {
            "brand": brand,
            "material": material,
            "density": 1.24,
            "diameter": 1.75
        },
        "print_settings": {
            "nozzle_temperature": temp_nozzle,
            "nozzle_temperature_initial_layer": temp_nozzle + 5,
            "bed_temperature": temp_bed,
            "bed_temperature_initial_layer": temp_bed,
            "cooling_fan_speed": 100
        }
    }
    return data, "filaments"

def create_process():
    print("\n--- Creating New Process ---")
    name = get_input("Display Name (e.g. Phantom Detail 0.16mm)")
    layer_height = float(get_input("Layer Height (mm)", "0.20"))
    infill = int(get_input("Infill Density (%)", "15"))
    speed_wall = int(get_input("Outer Wall Speed (mm/s)", "200"))
    
    file_id = f"{ID_PREFIX}{clean_id(name)}"
    
    data = {
        "schema_version": SCHEMA_VER,
        "type": "process",
        "id": file_id,
        "maintainer": MAINTAINER,
        "metadata": {
            "name": name,
            "description": f"Optimized by {MAINTAINER}"
        },
        "resolution": {
            "layer_height": layer_height,
            "first_layer_height": layer_height + 0.04,
            "line_width": 0.42
        },
        "structure": {
            "wall_loops": 3,
            "top_shell_layers": 4,
            "bottom_shell_layers": 3,
            "infill_density": infill,
            "infill_pattern": "grid"
        },
        "speed": {
            "outer_wall": speed_wall,
            "inner_wall": int(speed_wall * 1.5),
            "infill": int(speed_wall * 1.5),
            "top_surface": int(speed_wall * 0.75),
            "travel": 500
        }
    }
    return data, "processes"

def main():
    print("==========================================")
    print("   PHANTOM EDITION - PROFILE GENERATOR    ")
    print("==========================================")
    print("1. New Filament")
    print("2. New Process")
    print("Q. Quit")
    
    choice = input("\nSelect an option: ").upper()
    
    data = None
    folder = None
    
    if choice == '1':
        data, folder = create_filament()
    elif choice == '2':
        data, folder = create_process()
    elif choice == 'Q':
        return
    else:
        print("Invalid choice.")
        return

    # Create the file
    if data and folder:
        # Make sure folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        filename = f"{data['id']}.json"
        filepath = os.path.join(folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"\n✅ Success! Created: {filepath}")
        print(f"   ID: {data['id']}")

if __name__ == "__main__":
    main()