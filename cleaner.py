import os

def nettoyer_dossiers(dossier_parent: str):
    if not os.path.isdir(dossier_parent):
        print(f"Erreur : {dossier_parent} n'est pas un dossier valide.")
        return

    for sous_dossier in os.listdir(dossier_parent):
        chemin_sous_dossier = os.path.join(dossier_parent, sous_dossier)

        if os.path.isdir(chemin_sous_dossier):
            print(f"Traitement du dossier : {chemin_sous_dossier}")

            for fichier in os.listdir(chemin_sous_dossier):
                chemin_fichier = os.path.join(chemin_sous_dossier, fichier)

                if os.path.isfile(chemin_fichier) and not fichier.lower().endswith((".txt")):
                    print(f"Suppression : {chemin_fichier}")
                    os.remove(chemin_fichier)

nettoyer_dossiers(r"C:\Users\WMZY6987\OneDrive - orange.com\Documents\projet_trasncription\audio_original")
