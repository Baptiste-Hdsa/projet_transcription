import os
import shutil

def deplacer_trs_vers_racine(trs_root):
    if not os.path.isdir(trs_root):
        print(f"{trs_root} n'est pas un dossier valide.")
        return

    for root, dirs, files in os.walk(trs_root):
        if root == trs_root:
            continue

        for f in files:
            if f.lower().endswith(".trs"):
                source = os.path.join(root, f)
                destination = os.path.join(trs_root, f)

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

                shutil.move(source, destination)
                print(f"Déplacé : {source} -> {destination}")

    print("Déplacement terminé")


deplacer_trs_vers_racine(r"C:\Users\WMZY6987\OneDrive - orange.com\Documents\projet_trasncription\audio_trs")
