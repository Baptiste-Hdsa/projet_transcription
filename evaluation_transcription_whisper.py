import pandas as pd
import time
import jiwer
import openai
import os
import requests

# Load dataset from TSV file
dataset = pd.read_csv("dataset.tsv", sep="\t")

# API keys for each service
api_key_whisper = [""]
api_key_voxtral = [""]
api_key_cobalt = [""]

def transcribe_whisper():
    """
    Transcribe audio files using Whisper API and evaluate results.
    """
    client = openai.OpenAI(
        api_key=api_key_whisper
    )

    results = []

    for index, row in dataset.iterrows():
        reference_transcript = row["transcript"]
        filename = row["filename"]

        audio_path = os.path.join("audio_only", filename)

        start_time = time.time()

        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="openai/whisper-1",
                file=audio_file,
                response_format="text",
                language="fr"
            )
        predicted_transcript = response

        end_time = time.time()
        inference_time = end_time - start_time

        WER = jiwer.wer(reference_transcript, predicted_transcript)
        CER = jiwer.cer(reference_transcript, predicted_transcript)

        results.append({
            "filename": filename,
            "predicted_transcript": predicted_transcript,
            "inference_time": inference_time,
            "WER": WER,
            "CER": CER
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv(
        os.path.join("results", "results_whisper.tsv"),
        sep="\t",
        index=False
    )

    mean_wer = results_df['WER'].mean()
    std_wer = results_df['WER'].std()
    mean_cer = results_df['CER'].mean()
    std_cer = results_df['CER'].std()

    synthesis = [{
        "mean_wer": mean_wer,
        "std_wer": std_wer,
        "mean_cer": mean_cer,
        "std_cer": std_cer
    }]
    synthesis_df = pd.DataFrame(synthesis)
    synthesis_df.to_csv(
        os.path.join("synthesis", "synthesis_whisper.tsv"),
        sep="\t",
        index=False
    )

def transcribe_voxtral():
    """
    Transcribe audio files using Voxtral API and evaluate results.
    """
    api_key = api_key_voxtral
    model = "voxtral-mini-2507"
    url = "https://api.mistral.ai/v1/audio/transcriptions"

    results = []

    for index, row in dataset.iterrows():
        reference_transcript = row["transcript"]
        filename = row["filename"]

        audio_path = os.path.join("audio_only", filename)

        start_time = time.time()

        with open(audio_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {
                "model": model,
                "language": "fr"
            }
            headers = {"Authorization": f"Bearer {api_key}"}

            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            result = response.json()

        predicted_transcript = result.get("text", "")

        end_time = time.time()
        inference_time = end_time - start_time

        WER = jiwer.wer(reference_transcript, predicted_transcript)
        CER = jiwer.cer(reference_transcript, predicted_transcript)

        results.append({
            "filename": filename,
            "predicted_transcript": predicted_transcript,
            "inference_time": inference_time,
            "WER": WER,
            "CER": CER
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv(
        os.path.join("results", "results_voxtral.tsv"),
        sep="\t",
        index=False
    )

    mean_wer = results_df['WER'].mean()
    std_wer = results_df['WER'].std()
    mean_cer = results_df['CER'].mean()
    std_cer = results_df['CER'].std()

    synthesis = [{
        "mean_wer": mean_wer,
        "std_wer": std_wer,
        "mean_cer": mean_cer,
        "std_cer": std_cer
    }]
    synthesis_df = pd.DataFrame(synthesis)
    synthesis_df.to_csv(
        os.path.join("synthesis", "synthesis_voxtral.tsv"),
        sep="\t",
        index=False
    )

def transcribe_cobalt():
    """
    Transcribe audio files using Cobalt API and evaluate results.
    """
    api_key = api_key_cobalt
    model = "cobalt-fr-asr"
    url = "https://api.cobaltspeech.com/v1/transcribe"

    results = []

    for index, row in dataset.iterrows():
        reference_transcript = row["transcript"]
        filename = row["filename"]

        audio_path = os.path.join("audio_only", filename)

        start_time = time.time()

        with open(audio_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {
                "model": model,
                "language": "fr"
            }
            headers = {"Authorization": f"Bearer {api_key}"}

            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            result = response.json()

        predicted_transcript = result["results"][0]["transcript"]

        end_time = time.time()
        inference_time = end_time - start_time

        WER = jiwer.wer(reference_transcript, predicted_transcript)
        CER = jiwer.cer(reference_transcript, predicted_transcript)

        results.append({
            "filename": filename,
            "predicted_transcript": predicted_transcript,
            "inference_time": inference_time,
            "WER": WER,
            "CER": CER
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv(
        os.path.join("results", "results_cobalt.tsv"),
        sep="\t",
        index=False
    )

    mean_wer = results_df['WER'].mean()
    std_wer = results_df['WER'].std()
    mean_cer = results_df['CER'].mean()
    std_cer = results_df['CER'].std()

    synthesis = [{
        "mean_wer": mean_wer,
        "std_wer": std_wer,
        "mean_cer": mean_cer,
        "std_cer": std_cer
    }]
    synthesis_df = pd.DataFrame(synthesis)
    synthesis_df.to_csv(
        os.path.join("synthesis", "synthesis_cobalt.tsv"),
        sep="\t",
        index=False
    )