import os
import shutil

def deplacer_trs_vers_racine(trs_root):
    # Check if the provided path is a valid directory
    if not os.path.isdir(trs_root):
        print(f"{trs_root} is not a valid directory.")
        return

    for root, dirs, files in os.walk(trs_root):
        # Skip the root directory itself
        if root == trs_root:
            continue

        for f in files:
            # Check if the file is a .trs file
            if f.lower().endswith(".trs"):
                source = os.path.join(root, f)
                destination = os.path.join(trs_root, f)

                # If a file with the same name exists, create a new unique name
                if os.path.exists(destination):
                    base, ext = os.path.splitext(f)
                    i = 1
                    while True:
                        new_name = f"{base}_{i}{ext}"
                        new_dest = os.path.join(trs_root, new_name)
                        if not os.path.exists(new_dest):
                            destination = new_dest
                            break
                        i += 1

                # Move the file to the root directory
                shutil.move(source, destination)
                print(f"Moved: {source} -> {destination}")

    print("Move completed")

# Example usage: move .trs files to the root directory
deplacer_trs_vers_racine(r"C:\Users\WMZY6987\OneDrive - orange.com\Documents\projet_trasncription\audio_trs")