# step 3 - chunk the transcripts into smaller pieces for better searchability and context retrieval

import json
import os 

json_files = os.listdir("transcripts")



for json_file in json_files:
    all_chunks = []
    if "_" in json_file:
        file_name = json_file.rsplit(".", 1)[0]  
        number = json_file.split("_")[0]
        title = file_name.split("_")[1]

        with open(os.path.join("transcripts", json_file), "r") as f:
            result = json.load(f)

        output_path = f"chunks/{number}_{title}_chunks.json"
        
        
        if os.path.exists(output_path):
            print(f"{title} — chunks already exist")
            continue


        for segment in result["segments"]:
            chunk = {
                "number": number,
                "title": title,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            }
            all_chunks.append(chunk)

        print(f"Chunked: {title} -> {len(result['segments'])} chunks")

        os.makedirs("chunks", exist_ok=True)

        output_filename = f"chunks/{number}_{title}_chunks.json"
        with open(output_filename, "w") as f:
            json.dump({"chunks": all_chunks}, f, indent=2)

        print(f"Saved → {output_filename} ({len(all_chunks)} chunks)") 