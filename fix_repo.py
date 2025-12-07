import os
import json

# CONFIGURATION
# ---------------------------------------------------------
TARGET_DIR = "./profile-templates"  # Point this to your folder
MAINTAINER_NAME = "BlackPhantomm"
SCHEMA_VERSION = "1.0.0"

def update_filament_json(data):
    """Fixes filament files to match new schema."""
    # 1. Add Schema Version if missing
    if "schema_version" not in data:
        data["schema_version"] = SCHEMA_VERSION
    
    # 2. Add Maintainer
    data["maintainer"] = MAINTAINER_NAME
    
    # 3. Ensure Compatibility block exists
    if "compatibility" not in data:
        data["compatibility"] = {
            "printers": ["*"],
            "nozzles": ["0.4", "0.6"]
        }
    return data

def update_process_json(data):
    """Fixes process files by separating speed/resolution."""
    # 1. Add Schema Version
    if "schema_version" not in data:
        data["schema_version"] = SCHEMA_VERSION
        
    # 2. Add Maintainer
    data["maintainer"] = MAINTAINER_NAME
    
    # 3. Restructure 'settings' into 'resolution', 'structure', 'speed'
    # This looks for old mixed settings and sorts them into the new buckets
    if "settings" in data:
        settings = data.pop("settings") # Remove old block
        
        # Create new blocks if they don't exist
        if "resolution" not in data: data["resolution"] = {}
        if "structure" not in data: data["structure"] = {}
        if "speed" not in data: data["speed"] = {}
        
        # Lists of keys for the new categories
        resolution_keys = ["layer_height", "first_layer_height", "line_width"]
        structure_keys = ["wall_loops", "top_shell_layers", "bottom_shell_layers", "infill_density", "infill_pattern"]
        speed_keys = ["outer_wall", "inner_wall", "infill", "top_surface", "travel"]
        
        # Sort the keys
        for key, value in settings.items():
            if key in resolution_keys:
                data["resolution"][key] = value
            elif key in structure_keys:
                data["structure"][key] = value
            elif key in speed_keys:
                data["speed"][key] = value
            else:
                # Keep unknown keys in structure by default so they aren't lost
                data["structure"][key] = value
            
    return data

def process_files():
    print(f"Scanning directory: {TARGET_DIR}...")
    count = 0
    
    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Detect file type and update
                    is_updated = False
                    
                    # check if it is a filament file
                    if "filament" in file.lower() or data.get("type") == "filament":
                        data = update_filament_json(data)
                        is_updated = True
                        
                    # check if it is a process file
                    elif "process" in file.lower() or data.get("type") == "process":
                        data = update_process_json(data)
                        is_updated = True
                    
                    if is_updated:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2) # indent=2 makes it pretty readable
                        print(f"Fixed: {file}")
                        count += 1
                        
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    print(f"Done! Successfully updated {count} files.")

if __name__ == "__main__":
    process_files()