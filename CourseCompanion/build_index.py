import os
import glob
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_DIR = "data"
ARTIFACT_DIR = "artifacts"
MODEL_NAME = "all-MiniLM-L6-v2"

def load_documents():
    docs = []
    for path in glob.glob(os.path.join(DATA_DIR, "*.txt")):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        docs.append((os.path.basename(path), text))
    return docs

def split_into_chunks(text, max_chars=500):
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) + 1 <= max_chars:
            current = (current + " " + p).strip()
        else:
            if current:
                chunks.append(current)
            current = p
    if current:
        chunks.append(current)
    return chunks

def main():
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    model = SentenceTransformer(MODEL_NAME)

    all_chunks = []
    sources = []

    for filename, text in load_documents():
        chunks = split_into_chunks(text)
        for ch in chunks:
            all_chunks.append(ch)
            sources.append(filename)

    embeddings = model.encode(all_chunks, show_progress_bar=True)
    np.save(os.path.join(ARTIFACT_DIR, "embeddings.npy"), embeddings)

    with open(os.path.join(ARTIFACT_DIR, "chunks.txt"), "w", encoding="utf-8") as f:
        for src, ch in zip(sources, all_chunks):
            f.write(f"## {src}\n{ch}\n\n")

if __name__ == "__main__":
    main()
