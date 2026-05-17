#Step 1 of the RAG Pipeline
# COnverts the video to mp3
import os
import subprocess

files = os.listdir('videos')

# used enumerate with zfill(2) so the pipeline scales automatically to any number of videos without any code changes.
for index, file in enumerate(files, start=1):
    file_name = os.path.splitext(file)[0]        # Clean name without .mp4
    tutorial_number = str(index).zfill(2)        # Auto: 01, 02, 03

    output_path = f"audios/{tutorial_number}_{file_name}.mp3"

    if os.path.exists(output_path):
        print(f"{file_name} — audio already exists")
        continue

    os.makedirs("audios", exist_ok=True)

    print(tutorial_number, file_name)

    # subprocess.run() executes a terminal command from Python.
    # This is equivalent to running in terminal:
    #   ffmpeg -i "videos/filename.mp4" -q:a 0 -map a "audios/02_Title.mp3"

    subprocess.run([
        "ffmpeg",                       #→ the tool we're calling
        "-i", f"videos/{file}",         # → input flag; next arg is the input file,full path to the input video file
        "-q:a", "0",                    # → best audio quality (0 = highest, 9 = lowest)
        "-map", "a",                    #  → extract ONLY the audio stream (ignore video)
        f"audios/{tutorial_number}_{file_name}.mp3" # → output path; saves as numbered .mp3
                                                    #e.g. "audios/02_Your First HTML Website.mp3"

    ])