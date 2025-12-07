import os
import json

# CONFIGURATION
# ---------------------------------------------------------
TARGET_DIR = "."  
PREFIX = "phantom_"

def process_files():
    print(f"--- Starting Phantom ID Update in: {os.getcwd()} ---")
    files_updated = 0
    files_skipped = 0
    
    for root, dirs, files in os.walk(TARGET_DIR):
        if ".git" in root: continue 
            
        for file in files:
            if file.endswith(".json") and "template" not in file and file != "phantomize_ids.py":
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                        except:
                            print(f"[!] Skipped invalid JSON: {file}")
                            continue

                    # Check if 'id' exists
                    if "id" in data:
                        current_id = data["id"]
                        
                        # Only update if it doesn't already have the prefix
                        if not current_id.startswith(PREFIX):
                            new_id = f"{PREFIX}{current_id}"
                            data["id"] = new_id
                            
                            with open(file_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2)
                                
                            print(f"[+] Updated ID: {current_id} -> {new_id}")
                            files_updated += 1
                        else:
                            files_skipped += 1
                    else:
                        print(f"[-] No ID found in: {file}")

                except Exception as e:
                    print(f"[!] Error on {file}: {e}")

    print(f"------------------------------------------------")
    print(f"Scan Complete.")
    print(f"Updated {files_updated} files.")
    print(f"Skipped {files_skipped} files (already had prefix).")

if __name__ == "__main__":
    process_files()