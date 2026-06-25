# AI Teaching Assistant (RAG)

A Retrieval-Augmented Generation (RAG) system that transforms Hindi video lectures into an interactive English Q&A assistant. Ask questions about course material and get accurate answers grounded in actual video content — with timestamp citations so students know exactly where to find it in the video.

---

## What It Does

- Takes Hindi video lectures as input
- Extracts audio, transcribes and translates to English using Whisper
- Embeds transcripts into a ChromaDB vector store
- Answers student questions using semantic search + GROQ LLM
- Returns answers with timestamp citations (e.g. "1:15 - 2:30") linking back to the source video

---

## RAG Pipeline

```
Video Files (.mp4)
        ↓
process_videos.py — FFmpeg extracts audio → .mp3 files
        ↓
translate.py — Whisper transcribes Hindi audio + translates to English
        ↓
chunks.py — Splits transcripts into segment-level chunks with timestamps
        ↓
embed.py — Embeds chunks into ChromaDB with cosine similarity (HNSW)
        ↓
app.py — Flask web app: semantic search → GROQ LLM → answer + citations
```

---

## Project Structure

```
AI-Teaching/
├── app.py                  # Flask web app — search, answer generation, UI
├── process_videos.py       # Step 1: Video → Audio (.mp4 → .mp3 via FFmpeg)
├── translate.py            # Step 2: Audio → English transcript (Whisper)
├── chunks.py               # Step 3: Transcript → Segment chunks with timestamps
├── embed.py                # Step 4: Chunks → ChromaDB vector embeddings
├── video_mapping.json      # Persistent video numbering (survives re-runs)
├── templates/
│   └── index.html          # Frontend UI
├── videos/                 # Input video files (not tracked in git)
├── audios/                 # Extracted audio files (not tracked in git)
├── transcripts/            # Whisper JSON outputs
├── chunks/                 # Chunked transcript JSON files
├── vectorstore/            # ChromaDB persistent storage
├── .env                    # API keys (not committed to GitHub)
└── requirements.txt
```

---

## Key Technical Decisions

### Hindi → English Translation
Whisper is run with `language="hi"` and `task="translate"` — this simultaneously transcribes Hindi audio and translates it to English in one pass, making the system usable for English-speaking students on Hindi content.

### Persistent Video Numbering
`video_mapping.json` assigns stable numbers to videos across runs. Without this, re-running `process_videos.py` would re-number videos and break existing chunk/embed references.

### Duplicate Prevention
Both `embed.py` and `chunks.py` check if output already exists before processing — so re-running the pipeline never duplicates data in ChromaDB or overwrites existing chunks.

### Cosine Similarity
ChromaDB collection uses `"hnsw:space": "cosine"` explicitly — better for semantic text similarity than default L2 distance.

### Temperature 0.3
GROQ LLM called with `temperature=0.3` — low enough to stay factual and grounded in the retrieved context, not hallucinate.

### Refusal Prompt
System prompt explicitly instructs the model: *"If the answer is not in the context, say: I couldn't find that in the course material."* — prevents the model from answering from general knowledge outside the video content.

### Timestamp Citations
Every retrieved chunk carries `start` and `end` metadata from Whisper segments. These are formatted (e.g. `75.3 → "1:15"`) and returned with every answer so students can jump directly to the relevant video moment.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| FFmpeg | Video to audio extraction |
| OpenAI Whisper (small) | Speech recognition + Hindi to English translation |
| ChromaDB | Vector store with cosine similarity (HNSW) |
| GROQ API (llama-3.3-70b-versatile) | LLM answer generation |
| Flask | Web application framework |
| python-dotenv | API key management |

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/paragpawar0077/AI-Teaching-Assistant
cd AI-Teaching-Assistant
```

**2. Install dependencies**
```bash
pip install openai-whisper torch ffmpeg-python chromadb groq flask python-dotenv
```

**3. Install FFmpeg**

Windows: Download from https://ffmpeg.org/download.html and add to PATH

Mac:
```bash
brew install ffmpeg
```

Linux:
```bash
sudo apt install ffmpeg
```

**4. Add API key**

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```
Get a free key at: https://console.groq.com

**5. Add your videos**

Place `.mp4` files in the `videos/` folder.

---

## Running the Pipeline

```bash
# Step 1 — Extract audio
python process_videos.py

# Step 2 — Transcribe and translate
python translate.py

# Step 3 — Chunk transcripts
python chunks.py

# Step 4 — Embed into ChromaDB
python embed.py

# Step 5 — Run the web app
python app.py
```

Open `http://localhost:5000` in your browser.

---

## Sample Videos Used

The system was tested on 3 Hindi ML/AI lecture videos:
- Supervised, Unsupervised and Reinforcement Learning (Hindi)
- Machine Learning in 5 Minutes (Hindi)
- What is Generative AI? (Hindi)

---

## Known Limitations

- Uses Whisper segment-level chunking — overlapping chunk strategy would improve retrieval accuracy for long answers that span multiple segments
- Whisper `small` model used for speed — `large-v2` on GPU would give better transcription accuracy
- No reranking step — retrieved chunks are used directly without cross-encoder reranking
- Video files not included in repo due to size — pipeline must be run on your own videos

---

## Author

**Parag Pawar**
- GitHub: https://github.com/paragpawar0077
- Email: paragpawar0077@gmail.com