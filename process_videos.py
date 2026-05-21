import os
import subprocess
import json

files = sorted(os.listdir('videos'))

# Load existing mapping if it exists
mapping_path = "video_mapping.json"
if os.path.exists(mapping_path):
    with open(mapping_path, "r") as f:
        mapping = json.load(f) 
else:
    mapping = {}

# Assign numbers only to NEW videos
next_number = len(mapping) + 1

for file in files:
    file_name = os.path.splitext(file)[0]

    # If already in mapping, use existing number
    if file_name in mapping:
        tutorial_number = mapping[file_name]
    else:
        # New video — assign next number
        tutorial_number = str(next_number).zfill(2)
        mapping[file_name] = tutorial_number
        next_number += 1

    output_path = f"audios/{tutorial_number}_{file_name}.mp3"

    if os.path.exists(output_path):
        print(f"Skipping {file_name} — already exists")
        continue

    os.makedirs("audios", exist_ok=True)
    print(f"Processing: {tutorial_number} {file_name}")

    subprocess.run([
        "ffmpeg",
        "-i", f"videos/{file}",
        "-q:a", "0",
        "-map", "a",
        output_path
    ])
    print(f"Saved → {output_path}")

# Save updated mapping
with open(mapping_path, "w") as f:
    json.dump(mapping, f, indent=2)
print(f"Mapping saved → {mapping_path}")