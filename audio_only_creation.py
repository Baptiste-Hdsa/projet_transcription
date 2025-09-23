import os
import shutil

def move_audio_to_root(audio_root):
    """
    Move all .mp3 and .wav files from subdirectories to the root directory.
    If a file with the same name exists in the root, append a number to the filename.
    """
    for root, dirs, files in os.walk(audio_root):
        # Skip the root directory itself
        if root == audio_root:
            continue

        for file in files:
            # Check if the file is an audio file (.mp3 or .wav)
            if file.lower().endswith((".mp3", ".wav")):
                source = os.path.join(root, file)
                destination = os.path.join(audio_root, file)

                # If a file with the same name exists, create a new unique name
                if os.path.exists(destination):
                    base, ext = os.path.splitext(file)
                    i = 1
                    while True:
                        new_name = f"{base}_{i}{ext}"
                        new_dest = os.path.join(audio_root, new_name)
                        if not os.path.exists(new_dest):
                            destination = new_dest
                            break
                        i += 1

                # Move the file to the root directory
                shutil.move(source, destination)
                print(f"Moved: {source} -> {destination}")

    print("Move completed")

# Example usage: move audio files to the root directory
move_audio_to_root(r"C:\Users\WMZY6987\OneDrive - orange.com\Documents\projet_trasncription\audio_only")