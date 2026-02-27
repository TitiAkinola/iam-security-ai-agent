import shutil
import os
from datetime import datetime

def backup_files(source_dir, dest_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created destination directory: {dest_dir}")

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Iterate through files in source directory
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)

        # Only copy files (skip subfolders)
        if os.path.isfile(source_path):
            # Create new filename: original_name_20260203_143000.ext
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{timestamp}{ext}"
            dest_path = os.path.join(dest_dir, new_filename)

            # Copy and rename
            shutil.copy2(source_path, dest_path)
            print(f"✅ Backed up: {filename} -> {new_filename}")

if __name__ == "__main__":
    # Example paths - update these for your system
    source = "./source_data"
    destination = "./backups"
    
    # Create a dummy source folder for testing if it doesn't exist
    if not os.path.exists(source):
        os.makedirs(source)
        with open(f"{source}/test_log.txt", "w") as f:
            f.write("Sample log data for backup.")

    backup_files(source, destination)
