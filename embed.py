import json
import os
import chromadb

client = chromadb.PersistentClient(path ="vectorstore/")

collection = client.get_or_create_collection(
    name = "video_tutorials",
    metadata = {"hnsw:space": "cosine"}
)

json_files = [file for file in os.listdir("chunks") if file.endswith("_chunks.json")]

for json_file in json_files:

    title = json_file.replace("_chunks.json", "")  # Extract title from filename

    existing = collection.get(where={"title": title})
    if len(existing["ids"])>0:
        print(f"{title} already exists in the collection, skipping.")
        continue

    with open(f"chunks/{json_file}", "r") as f:
        data = json.load(f)

    chunks = data["chunks"]
    print(f" Embedding: {title} with {len(chunks)} chunks...")

    documents =[]
    metadatas =[]
    ids = []

    for i ,chunk in enumerate(chunks):
        documents.append(chunk["text"])
        metadatas.append({
            "number":chunk["number"],
            "title": chunk["title"],
            "start": str(chunk["start"]),
            "end": str(chunk["end"])
        })

        ids.append(f"{title}_{i}")

    collection.add(
        documents = documents,
        metadatas = metadatas,
        ids = ids
    )

    print(f" Embedded:{len(chunks)} chunks for {title} into the chromadb collection. ")

    total = collection.count()
    print(f" Total chunks in collection: {total}")
    print("saved to vectorestore/ directory")