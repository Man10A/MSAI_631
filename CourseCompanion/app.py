import gradio as gr
from rag_engine import answer_with_rag

def chat_fn(message, history):
    reply = answer_with_rag(message)
    return reply

demo = gr.ChatInterface(
    fn=chat_fn,
    title="Course Companion Chatbot (RAG + Groq)",
    description="Ask about syllabus, assignments, and topics."
)

if __name__ == "__main__":
    demo.launch()
