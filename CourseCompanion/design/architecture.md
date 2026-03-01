```mermaid

flowchart TB
    User["Student\n(browser)"]
    UI["Gradio UI\n(app.py)"]
    RAG["RAG Engine\n(rag_engine.py)"]
    Artifacts["artifacts/\nembeddings.npy,\nchunks.txt"]
    Data["Course docs\n(data/: syllabus,\nassignments, topics)"]
    LLM["Groq LLM\n(API)"]

    User -->|"Question"| UI
    UI -->|"call answer_with_rag()"| RAG
    RAG -->|"read embeddings\n+ chunks"| Artifacts
    Artifacts --- Data
    RAG -->|"send question\n+ retrieved context"| LLM
    LLM -->|"Answer text"| UI
    UI -->|"Chat reply"| User

  ...