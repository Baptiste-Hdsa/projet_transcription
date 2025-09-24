from mutagen import File as MutagenFile
import os
import xml.etree.ElementTree as ET
import re
import pandas as pd
from glob import glob

def get_audio_info(filepath):
    """
    Extract audio file information using mutagen.
    Returns filename, duration (seconds), extension, and sample rate.
    """
    audio = MutagenFile(filepath)
    if audio is None or not audio.info:
        raise ValueError(f"Cannot read audio info: {filepath}")
    
    duration = audio.info.length  # duration in seconds
    sr = getattr(audio.info, "sample_rate", None)  # some mp3 files may not have sample rate info
    ext = os.path.splitext(filepath)[1].lstrip(".")
    
    return os.path.basename(filepath), duration, ext, sr

"""
Alternative using librosa (commented out):
import librosa
import os

def get_audio_info(filepath):
    # Returns filename, duration, extension, sample rate using librosa
    y, sr = librosa.load(filepath, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    return os.path.basename(filepath), duration, os.path.splitext(filepath)[1].replace(",", ""), sr
"""

def parse_trs(trs_file):
    """
    Parse a .trs XML file and return a list of speakers and the full transcript.
    """
    tree = ET.parse(trs_file)  # Load XML tree from file
    root = tree.getroot()      # Get root element

    speakers = []  # List of all speakers (name or id)
    speakers_elem = root.find("Speakers")
    if speakers_elem is not None:
        for spk in speakers_elem:
            name = spk.attrib.get("name")
            if not name:
                name = spk.attrib.get("id", "unknown") 
            speakers.append(name)

    transcript_parts = []
    for turn in root.findall(".//Turn"):
        text = "".join(turn.itertext())  # Get text without tags
        text = re.sub(r'<[^>]+>', ' ', text)
        text = text.strip()  # Remove unnecessary spaces, newlines, tabs at start/end
        if text:
            transcript_parts.append(text)

    transcript = " ".join(transcript_parts)  # Join all parts into a single string
    transcript = " ".join(transcript.split())  # Replace multiple spaces with single space
    
    return speakers, transcript

def build_dataset(audio_dir, trs_dir, output="dataset.tsv"):
    """
    Build a dataset by matching audio files and .trs files.
    Save the result as a TSV file.
    """
    rows = []
    
    for audio_file in glob(os.path.join(audio_dir, "*")):
        filename, duration, fmt, sr = get_audio_info(audio_file)
        
        trs_file = os.path.join(trs_dir, os.path.splitext(filename)[0] + ".trs")
        if not os.path.exists(trs_file):
            print(f"No .trs file for {filename}, skipping")
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
    print(f"Dataset saved to {output}")

# Build the dataset using audio and .trs directories
build_dataset(audio_dir="audio_only", trs_dir="audio_trs", output="dataset.tsv")