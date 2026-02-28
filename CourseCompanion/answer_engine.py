# answer_engine.py

# Very simple FAQ-based answer engine for the Course Companion Chatbot.
# You can expand the FAQ list with more (keywords, answer) pairs.

FAQ = [
    (
        "when is class",
        "Class meets on the scheduled days and times listed in the course syllabus."
    ),
    (
        "grading policy",
        "Grades are based on homework, projects, and exams as described in the syllabus."
    ),
    (
        "group project",
        "The group project has five parts: proposal, design document, source code in Git, results paper, and presentation."
    ),
    (
        "office hours",
        "Office hours are listed in the syllabus; contact the instructor if you need the latest schedule."
    ),
    (
        "late policy",
        "The late submission policy is described in the syllabus; please review that section for details."
    ),
]

def find_best_answer(question: str) -> str:
    """
    Very simple keyword matching:
    - Lowercases the user question.
    - For each FAQ entry, counts how many words from the keyword string appear in the question.
    - Returns the answer with the highest score, or a fallback if nothing matches.
    """
    q = question.lower()
    best_score = 0
    best_answer = None

    for kw, answer in FAQ:
        keywords = kw.lower().split()
        score = sum(1 for word in keywords if word in q)
        if score > best_score:
            best_score = score
            best_answer = answer

    if best_answer is None:
        return "I am not sure. Please check the syllabus or ask the instructor."
    return best_answer
