import os

def clean_folders(parent_folder: str):
    # Check if the provided path is a valid directory
    if not os.path.isdir(parent_folder):
        print(f"Error: {parent_folder} is not a valid directory.")
        return

    # Iterate through all subdirectories in the parent directory
    for subfolder in os.listdir(parent_folder):
        subfolder_path = os.path.join(parent_folder, subfolder)

        if os.path.isdir(subfolder_path):
            print(f"Processing folder: {subfolder_path}")

            # Iterate through all files in the subdirectory
            for file in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file)

                # Delete files that are not .txt files
                if os.path.isfile(file_path) and not file.lower().endswith(".txt"):
                    print(f"Deleting: {file_path}")
                    os.remove(file_path)

# Example usage: clean subfolders by removing non-.txt files
clean_folders(r"C:\Users\WMZY6987\OneDrive - orange.com\Documents\projet_trasncription\audio_original")