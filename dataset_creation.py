from mutagen import File as MutagenFile
import os
import xml.etree.ElementTree as ET
import re
import pandas as pd
from glob import glob

def audio_info(filepath):
    audio = MutagenFile(filepath)
    if audio is None or not audio.info:
        raise ValueError(f"Impossible de lire infos audio: {filepath}")
    
    duration = audio.info.length  # durée en secondes
    sr = getattr(audio.info, "sample_rate", None)  # certains mp3 n’ont pas d’info de sr
    ext = os.path.splitext(filepath)[1].lstrip(".")
    
    return os.path.basename(filepath),duration, ext, sr

"""
import librosa
import os

def audio_info(filepath): #fonction qui envoie le filename,duration,extension,taux d'échantillonage(sample_rate)
    y, sr = librosa.load(filepath,sr=None)
    duration = librosa.get_duration(y=y,sr=sr)
    return os.path.basename(filepath),duration, os.path.splitext(filepath)[1].replace(",",""),sr
"""


def parse_trs(trs_file): #fonction qui renvoie un tableau des locuteurs et un tableau contenant juste un élement qui est tout le transcript du fichier .trs soit un xml
    tree = ET.parse(trs_file) #varible qui représente l'intrégralité du doc sous forme d'un arbre d'élements en mémoire
    root = tree.getroot() #accès à la racine de tree

    speakers = [] #tableau de tout les locuteurs avec leurs nom ou id
    speakers_elem = root.find("Speakers")
    if speakers_elem is not None:
        for spk in speakers_elem:
            name = spk.attrib.get("name")
            if not name:
                name = spk.attrib.get("id","unknown") 
            speakers.append(name)

    transcript_parts = []
    for turn in root.findall(".//Turn"):
        text = "".join(turn.itertext()) #recupère le texte sans balises
        text = re.sub(r'<[^>]+>', ' ', text)
        text = text.strip()#retire les espaces, les sauts de ligne ou les tabulations inutiles au début et à la fin de la chaîne de texte
        if text:
            transcript_parts.append(text)

    transcript = " ".join(transcript_parts) #regroupe toute les parties en une chaine de charactère
    transcript = " ".join(transcript.split())  #juste remplace les espaces multiples par des simples
    
    return speakers, transcript


def build_dataset(audio_dir, trs_dir, output="dataset.tsv"):
    rows = []
    
    for audio_file in glob(os.path.join(audio_dir, "*")):
        filename, duration, fmt, sr = audio_info(audio_file)
        
        trs_file = os.path.join(trs_dir, os.path.splitext(filename)[0] + ".trs")
        if not os.path.exists(trs_file):
            print(f"Pas de fichier .trs pour {filename}, skip")
            continue
        
        speakers, transcript = parse_trs(trs_file)
        
        rows.append({
            "filename": filename,
            "duration": round(duration/60, 2),
            "format": fmt,
            "sample_rate": sr,
            "speakers": ",".join(speakers),
            "transcript": transcript
        })
    
    df = pd.DataFrame(rows)
    df.to_csv(output, sep="\t", index=False)
    print(f"Dataset sauvegardé dans {output}")


build_dataset(audio_dir="audio_only", trs_dir="audio_trs", output="dataset.tsv")