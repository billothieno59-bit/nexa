import os
import shutil

# Directories and extensions to remove safely (git folder excluded to protect repo history)
IGNORE_DIRS = {"__pycache__", ".pytest_cache"}
IGNORE_EXTS = {".pyc", ".pyo"}


def purge_transient_files(root_dir="."):
    for current_root, dirs, files in os.walk(root_dir, topdown=False):
        # Remove matching cache files
        for file in files:
            if any(file.endswith(ext) for ext in IGNORE_EXTS):
                file_path = os.path.join(current_root, file)
                try:
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")
                except Exception as e:
                    print(f"Error removing file {file_path}: {e}")

        # Remove matching cache directories
        for d in dirs:
            if d in IGNORE_DIRS:
                dir_path = os.path.join(current_root, d)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Removed directory: {dir_path}")
                except Exception as e:
                    print(f"Error removing directory {dir_path}: {e}")


if __name__ == "__main__":
    print("Purging build artifacts and transient cache files...")
    purge_transient_files()
    print("Cleanup complete.")
