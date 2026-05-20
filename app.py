from flask import Flask, request, jsonify, render_template
from groq import Groq
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# PersistentClient loads existing vectorstore from disk
chroma_client = chromadb.PersistentClient(path="vectorstore/")

collection = chroma_client.get_or_create_collection(
    name="video_tutorials",
)

# Converts raw seconds to readable timestamp
# e.g. 75.3 → "1:15" — shown to user as video citation
def format_time(seconds):
    seconds = int(float(seconds))
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/ask", methods=["POST"])
def ask():
    
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400


    # Query ChromaDB with the student's question
    # This is the RETRIEVAL step in RAG
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    
    chunks    = results["documents"][0]    
    metadatas = results["metadatas"][0]    


    context = ""
    sources = []

    for i, (chunk, meta) in enumerate(zip(chunks, metadatas)):
        start = format_time(meta["start"])
        end   = format_time(meta["end"])
        title = meta["title"]

        context += f"[Source {i+1}: {title} | {start} - {end}]\n{chunk}\n\n"
        sources.append({
            "title": title,
            "start": start,
            "end":   end
        })


    system_prompt = """You are a helpful AI Teaching Assistant for a Data Science and Machine Learning course.
You will be given context extracted from video lectures.
Answer the student's question using ONLY the provided context.
If the answer is not in the context, say: "I couldn't find that in the course material."
Always be clear, educational, and concise.
Mention the source timestamps so students know where to find it in the video."""

    user_prompt = f"""Context from course videos:
{context}

Student's Question: {question}

Please answer based only on the context above."""


    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ],
        temperature=0.3,    # low temp = more factual, less creative
        max_tokens=1024
    )

    answer = response.choices[0].message.content

    return jsonify({
        "answer":  answer,
        "sources": sources   # timestamps shown as citations in UI
    })


if __name__ == "__main__":
    
    app.run(debug=True)
