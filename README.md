#  RAG AI – Video Lecture Teaching Assistant

A **Retrieval-Augmented Generation (RAG)** based AI Teaching Assistant that transforms video lectures into an interactive Q&A system. Ask questions about your course material and get accurate, context-aware answers grounded in the actual video content.

---

##  How It Works (RAG Pipeline)

```text
[Video Files]
      ↓
process_videos.py
      ↓ Extracts audio (.mp3) using FFmpeg
translate.py
      ↓ Transcribes + translates audio to English using Whisper
chunks.py
      ↓ Splits transcript into smaller chunks for retrieval
[Vector Store]
      ↓ Chunks stored as searchable embeddings
[RAG Chat App]
      ↓ User asks question → Retrieve relevant chunks →  answeGROQrs
```

---

##  Project Structure

```text
RAG_AI/
├── videos/              # Input video files (not tracked in git)
├── audios/              # Extracted .mp3 files (not tracked in git)
├── jsons/               # Whisper transcription outputs
├── process_videos.py    # Step 1: Video → Audio extraction
├── translate.py         # Step 2: Audio → English transcript
├── chunks.py            # Step 3: Transcript → Chunks
└── .gitignore
```

---

##  Tech Stack

| Tool | Purpose |
|-------|----------|
| Python | Core language |
| FFmpeg | Video to audio extraction |
| OpenAI Whisper | Speech recognition + translation |
| GROQ | AI answer generation |
| ChromaDB | Vector storage for embeddings |

---

##  Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/RAG_AI.git
cd RAG_AI
```

### 2. Install dependencies

```bash
pip install openai-whisper torch ffmpeg-python langchain anthropic
```

### 3. Install FFmpeg

**Windows:** Download FFmpeg from https://ffmpeg.org/download.html and add it to PATH.

**Mac:**

```bash
brew install ffmpeg
```

**Linux:**

```bash
sudo apt install ffmpeg
```

### 4. Add your video

Place your video files inside:

```text
videos/
```

---

##  Running the Pipeline

### Step 1 — Extract audio from video

```bash
python process_videos.py
```

Converts all videos in `videos/` into `.mp3` files and stores them in `audios/`.

---

### Step 2 — Transcribe & translate

```bash
python translate.py
```

Uses Whisper (`small` model) to transcribe audio and translate it into English.

Outputs are stored in:

```text
jsons/
```

---

### Step 3 — Chunk transcript

```bash
python chunks.py
```

Splits transcripts into smaller overlapping chunks for embedding and retrieval.

---

##  Key Design Decisions

- Uses Whisper `small` model for local demos. For production systems, switch to `large-v2` on GPU for better accuracy.
- `exist_ok=True` prevents folder creation errors during repeated runs.
- FFmpeg `-map a` extracts only audio streams and ignores video data for faster processing.

---

##  Notes

- Videos and generated audio files are excluded from Git because of large file sizes.
- JSON transcripts are stored for inspection without rerunning Whisper.
- To check GPU availability:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

##  Author

**Parag Pawar**

- GitHub: (https://github.com/paragpawar0077)
- LinkedIn: (https://www.linkedin.com/in/parag-pawar-5383693a5/)
