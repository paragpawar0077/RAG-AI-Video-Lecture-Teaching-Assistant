# 🎓 RAG AI – Video Lecture Teaching Assistant
 
A **Retrieval-Augmented Generation (RAG)** based AI Teaching Assistant that transforms video lectures into an interactive Q&A system. Ask questions about your course material and get accurate, context-aware answers grounded in the actual video content.

## 📌 Notes
 
- Videos and audios are excluded from git (see `.gitignore`) due to large file sizes
- JSON transcripts are tracked so reviewers can see pipeline output without running Whisper
- To check if GPU acceleration is available for faster Whisper inference:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```
