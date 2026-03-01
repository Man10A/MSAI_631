```mermaid
flowchart TB
    subgraph Offline["Offline indexing"]
        Docs["data/*.txt\n(syllabus, assignments, topics)"]
        Split["Split into\nchunks"]
        Embed["Embed chunks\nall-MiniLM-L6-v2"]
        Artifacts["artifacts/\nembeddings.npy\nchunks.txt"]
        Docs --> Split --> Embed --> Artifacts
    end

    subgraph Online["Runtime QA"]
        Q["Student\nquestion"]
        QEmb["Embed\nquestion"]
        Search["Search\nembeddings"]
        TopK["Top-k\nchunks"]
        Prompt["Prompt\nGroq LLM"]
        Ans["Answer to\nchat UI"]
        Q --> QEmb --> Search --> TopK --> Prompt --> Ans
    end
  ...