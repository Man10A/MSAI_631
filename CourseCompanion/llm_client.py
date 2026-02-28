import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL_NAME = "llama-3.3-70b-versatile"  # free, general chat model at Groq[web:178][web:180]

SYSTEM_PROMPT = (
    "You are a helpful Course Companion chatbot for an AI/HCI class. "
    "You receive a student's question and a base answer taken from the syllabus or assignments. "
    "Rewrite the base answer clearly and politely. "
    "Do NOT invent new policies, grading rules, or dates. "
    "If the base answer says 'I am not sure', just encourage the student to check the syllabus or ask the instructor."
)

def improve_answer(user_question: str, base_answer: str) -> str:
    if not base_answer:
        base_answer = "I am not sure. Please check the syllabus or ask the instructor."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Question: {user_question}\nBase answer: {base_answer}",
        },
    ]

    chat_completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
    )

    return chat_completion.choices[0].message.content.strip()
