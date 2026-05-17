import os
import whisper
import json

# Load Whisper model (small = faster, good enough for demo)
model = whisper.load_model("small")

# Get all .mp3 files from audios folder
audio_files = os.listdir("audios")

# Loop through each audio file
for audio_file in audio_files:

    if '_' in audio_file:
        output_path = f"jsons/{audio_file.replace('.mp3', '.json')}"
        if os.path.exists(output_path):
            print(f"{audio_file} — transcript already exists")
            continue

    audio_path = os.path.join("audios", audio_file)

    print(f"Transcribing: {audio_file}...")

    result = model.transcribe(audio_path, language="hi", task="translate")

    # Save the transcript as a JSON file in jsons/ folder
    # so chunks.py can pick it up in the next step
    os.makedirs("jsons", exist_ok=True)

    output_path = os.path.join("jsons", f"{os.path.splitext(audio_file)[0]}.json")

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Saved → {output_path}")