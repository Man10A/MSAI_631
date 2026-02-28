import os
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq

ARTIFACT_DIR = "artifacts"
MODEL_NAME_EMB = "all-MiniLM-L6-v2"
MODEL_NAME_LLM = "llama-3.3-70b-versatile"

# Load embeddings and chunks into memory
_embeddings = np.load(os.path.join(ARTIFACT_DIR, "embeddings.npy"))
_chunks = []
with open(os.path.join(ARTIFACT_DIR, "chunks.txt"), "r", encoding="utf-8") as f:
    current = []
    for line in f:
        if line.startswith("## "):
            continue
        elif line.strip() == "":
            if current:
                _chunks.append(" ".join(current).strip())
                current = []
        else:
            current.append(line.strip())
    if current:
        _chunks.append(" ".join(current).strip())

_emb_model = SentenceTransformer(MODEL_NAME_EMB)
_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = (
    "You are a helpful Course Companion chatbot for an AI/HCI class. "
    "You receive a student's question and some relevant course text. "
    "Answer clearly and concisely using only the provided context. "
    "If the context does not contain the answer, say you are not sure and suggest checking the syllabus or asking the instructor."
)

def retrieve_context(question: str, top_k: int = 3):
    q_emb = _emb_model.encode([question])[0]
    sims = _embeddings @ q_emb / (
        np.linalg.norm(_embeddings, axis=1) * np.linalg.norm(q_emb) + 1e-8
    )
    idxs = np.argsort(-sims)[:top_k]
    return [_chunks[i] for i in idxs]

def answer_with_rag(question: str) -> str:
    context_chunks = retrieve_context(question, top_k=3)
    context_text = "\n\n".join(context_chunks)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Question: {question}\n\nContext:\n{context_text}",
        },
    ]

    chat_completion = _client.chat.completions.create(
        model=MODEL_NAME_LLM,
        messages=messages,
    )

    return chat_completion.choices[0].message.content.strip()
