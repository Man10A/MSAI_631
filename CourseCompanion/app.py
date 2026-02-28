import gradio as gr
from rag_engine import answer_with_rag

EXAMPLES = [
    "What percent of the final grade is the HCI group project in MSAI-631?",
    "What are the required deliverables for the HCI group project in MSAI-631?",
    "What is the minimum passing grade listed for MSAI-631?",
    "What is the late work policy for assignments in MSAI-631?",
    "What does human-centered AI mean?",
]

def chat_fn(message, history):
    q = (message or "").strip().lower()
    if not q:
        return "Hi! I’m the Course Companion chatbot for MSAI-631. Ask me about grading, deadlines, or the HCI group project."

    if q in {"hi", "hello", "hey"}:
        return "Hello! What would you like to know about MSAI-631?"

    if "thank" in q:
        return "You’re welcome!"

    return answer_with_rag(message)

demo = gr.ChatInterface(
    fn=chat_fn,
    title="MSAI-631 Course Companion",
    description=(
        "Hello! I'm your MSAI-631 Course Companion. I can help with questions "
        "about your course information, assignments, grading, key topics, and the HCI group project.\n\n"
        "Click one of the example questions below or type your own."
    ),
    examples=EXAMPLES,
)

if __name__ == "__main__":
    demo.launch()
