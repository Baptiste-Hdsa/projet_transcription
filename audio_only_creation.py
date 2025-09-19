import os
import shutil

def deplacer_audio_vers_racine(audio_root):
    for root, dirs, files in os.walk(audio_root):
        if root == audio_root:
            continue

        for f in files:
            if f.lower().endswith((".mp3", ".wav")):
                source = os.path.join(root, f)
                destination = os.path.join(audio_root, f)

                if os.path.exists(destination):
                    base, ext = os.path.splitext(f)
                    i = 1
                    while True:
                        new_name = f"{base}_{i}{ext}"
                        new_dest = os.path.join(audio_root, new_name)
                        if not os.path.exists(new_dest):
                            destination = new_dest
                            break
                        i += 1

                shutil.move(source, destination)
                print(f"Déplacé : {source} -> {destination}")

    print("Déplacement terminé")

deplacer_audio_vers_racine(r"C:\Users\WMZY6987\OneDrive - orange.com\Documents\projet_trasncription\audio_only")
