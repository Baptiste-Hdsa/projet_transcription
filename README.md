# Audio Transcription and Benchmark Project

This project processes the **CFPP2000 corpus** (spoken French from Paris, 2000s). Audio files and their XML transcription files were obtained from the [CoCoON platform](https://cocoon.huma-num.fr). The `dataset_creation.py` script converts each XML transcription into a single line per transcript, producing `dataset.tsv` for further processing.

The main script transcribes the audio files using three different speech-to-text services: **Whisper (OpenAI-compatible API)**, **Voxtral**, and **Cobalt**. It calculates **Word Error Rate (WER)** and **Character Error Rate (CER)** for each transcription, saves the results in TSV files, and serves as a **benchmark to evaluate which service performs best** on this corpus.

## Usage

Run the dataset creation script first:

python dataset_creation.py

Then run the main transcription script to generate predictions and evaluation, for example by calling:

transcribe_whisper()  
transcribe_voxtral()  
transcribe_cobalt()

The scripts produce TSV files for each service with the following columns:
- `filename` : audio file name
- `predicted_transcript` : transcription output
- `inference_time` : processing time per audio
- `WER` : Word Error Rate
- `CER` : Character Error Rate

## Example output for results

| filename                    | predicted_transcript                 | inference_time | WER  | CER  |
|-----------------------------|-------------------------------------|----------------|------|------|
| Alice_Cherviel_F_28_17e.mp3 | et voilà + bon alors ma première question | 12.34          | 0.05 | 0.02 |

## Example output for synthesis (benchmark)

| metric      | whisper | voxtral | cobalt |
|------------|--------|--------|--------|
| mean_WER   | 0.05   | 0.06   | 0.04   |
| std_WER    | 0.01   | 0.02   | 0.01   |
| mean_CER   | 0.02   | 0.03   | 0.02   |
| std_CER    | 0.01   | 0.01   | 0.01   |

## Notes
- Audio files are not located locally in the project folder ([download the audios](https://cocoon.huma-num.fr))
- API keys are required for Whisper, Voxtral, and Cobalt and must be set in the script
- `dataset_creation.py` is necessary to convert XML files into a single line per transcript before running the transcription functions
- The synthesis files allow for **benchmarking the three transcription services** to determine which is most accurate and efficient
