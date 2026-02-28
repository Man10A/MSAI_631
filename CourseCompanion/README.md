# Course Companion Chatbot (RAG + Groq)

A small Course Companion Chatbot for MSAI‑631 that answers questions about the syllabus, assignments, and key topics using a Retrieval‑Augmented Generation (RAG) pipeline and a Groq‑hosted LLM. [semaphore](https://semaphore.io/blog/rag-chatbot)

***

## 1. Project Structure

```text
CourseCompanion/
  app.py
  answer_engine.py        # (optional, for simple FAQ logic)
  llm_client.py           # (optional, earlier version)
  rag_engine.py           # retrieval + Groq LLM
  build_index.py          # builds embeddings index from data/
  data/
    syllabus.txt
    assignments.txt
    topics.txt
  artifacts/
    embeddings.npy        # created by build_index.py
    chunks.txt            # created by build_index.py
  README.md
```

***

## 2. Prerequisites

- Python 3.9+ installed
- Groq API key (free) from https://console.groq.com/keys [console.groq](https://console.groq.com/keys)
- Internet access (for first‑time model download and Groq API calls)

***

## 3. Environment setup

From the `CourseCompanion` folder:

```bash
# Optional: create virtual environment
python -m venv .venv

# Activate (PowerShell on Windows)
.venv\Scripts\activate

# Install dependencies
pip install gradio sentence-transformers numpy groq
```

***

## 4. Configure Groq API key

Get your key from the Groq console. [console.groq](https://console.groq.com/docs/quickstart)

Set it as an environment variable (Windows PowerShell):

```powershell
setx GROQ_API_KEY "YOUR_KEY_HERE"
```

Then **close and reopen** PowerShell so the variable is available, and verify:

```powershell
echo $env:GROQ_API_KEY
```

You should see your key (or at least a non‑empty value). [console.groq](https://console.groq.com/docs/overview)

***

## 5. Prepare course data

Edit the three files under `data/`:

- `data/syllabus.txt` – syllabus details (structure, grading, late policy, office hours).  
- `data/assignments.txt` – assignment and group project descriptions, timelines. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/136590091/696ee377-8f78-4587-a0be-40531d1959ef/Group-Project.docx)
- `data/topics.txt` – short explanations of key concepts (design thinking, human‑centered AI, multimodal interaction, RAG). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/136590091/da24dbdc-6f64-49cf-b412-e5909cfc1a05/Design-Thinking-Surendra-Varma-Mantena.docx)

You can use or modify the example content already in these files.

***

## 6. Build the embeddings index

Run from the project root:

```powershell
cd C:\Users\Suri\MSAI_631\CourseCompanion
python build_index.py
```

This will:

- Read all `.txt` files from `data/`.  
- Split them into chunks.  
- Compute embeddings using `sentence-transformers/all-MiniLM-L6-v2`. [geeksforgeeks](https://www.geeksforgeeks.org/nlp/what-is-text-embedding/)
- Write `artifacts/embeddings.npy` and `artifacts/chunks.txt`.

If you edit the data files later, re‑run `build_index.py`.

***

## 7. Run the chatbot

From the same folder:

```powershell
python app.py
```

You should see:

```text
Running on local URL:  http://127.0.0.1:7860
```

Open that URL in your browser.

Try questions like:

- “What is the late submission policy?”  
- “What are the five parts of the group project?” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/136590091/696ee377-8f78-4587-a0be-40531d1959ef/Group-Project.docx)
- “Explain design thinking in simple words.” [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/136590091/da24dbdc-6f64-49cf-b412-e5909cfc1a05/Design-Thinking-Surendra-Varma-Mantena.docx)
- “What is retrieval‑augmented generation (RAG)?” [semaphore](https://semaphore.io/blog/rag-chatbot)

The app uses:

- `rag_engine.answer_with_rag(question)`  
  - Embeds the question, retrieves top‑k relevant chunks from `artifacts/`.  
  - Calls Groq’s LLaMA model with the question + retrieved context.  
  - Returns a grounded answer. [console.groq](https://console.groq.com/docs/text-chat)

***

## 8. Notes and limitations

- This chatbot only knows what is in the `data/` text files.  
- It is **not** connected to the real LMS or grading system.  
- The LLM is instructed to answer using only provided context and not invent new policies.  
- Everything runs locally except the Groq API call; no course data is sent anywhere except the text you include in the prompt. [console.groq](https://console.groq.com/docs/quickstart)

You can extend the system by adding more `.txt` files under `data/` (e.g., `project_guidelines.txt`), then rerunning `build_index.py`.