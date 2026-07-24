"""
gemini_client.py — thin wrapper around Google's Gemini API for the
student AI Study Tools (notes, worksheets, study plans, flashcards).

Requires: pip install google-genai
Get a free API key at https://aistudio.google.com/apikey
"""

import json
import re

from google import genai

# Change this if Google renames or retires this model in the future.
DEFAULT_MODEL = "gemini-3.6-flash"

# Cap on how much book text we inject into a single prompt. Gemini Flash can
# handle far more, but keeping this modest keeps prompts fast and cheap.
MAX_CONTEXT_CHARS = 12000


def _client(api_key: str) -> genai.Client:
    if not api_key:
        raise ValueError("No Gemini API key configured. Ask an admin to add one in the Admin panel.")
    return genai.Client(api_key=api_key)


def _generate(prompt: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    client = _client(api_key)
    response = client.models.generate_content(model=model, contents=prompt)
    return (response.text or "").strip()


def _extract_json(text: str):
    """Gemini sometimes wraps JSON in ```json fences — strip them before parsing."""
    cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)


def select_relevant_excerpt(book_text: str, topic: str, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """
    Pick the passages of a book most relevant to `topic` so we don't have to
    send the whole book to the model. Simple keyword-frequency scoring per
    paragraph — good enough without needing a vector database.
    """
    if not book_text:
        return ""

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", book_text) if p.strip()]
    if not paragraphs:
        return book_text[:max_chars]

    keywords = [w.lower() for w in re.findall(r"\w+", topic) if len(w) > 2]

    def score(paragraph: str) -> int:
        lower = paragraph.lower()
        return sum(lower.count(kw) for kw in keywords)

    if keywords and any(score(p) > 0 for p in paragraphs):
        scored = sorted(paragraphs, key=score, reverse=True)
    else:
        scored = paragraphs  # no keyword matches — fall back to the start of the book

    excerpt_parts = []
    total = 0
    for p in scored:
        if total + len(p) > max_chars:
            break
        excerpt_parts.append(p)
        total += len(p)

    if not excerpt_parts:
        return book_text[:max_chars]

    return "\n\n".join(excerpt_parts)


def _with_context(instruction: str, context_text: str) -> str:
    if not context_text:
        return instruction
    return (
        f"{instruction}\n\n"
        "Base your answer primarily on the following source material. Stay faithful to it, "
        "and only add general knowledge to fill small gaps:\n"
        "-----BEGIN SOURCE MATERIAL-----\n"
        f"{context_text}\n"
        "-----END SOURCE MATERIAL-----"
    )


def generate_notes(topic: str, grade: str, api_key: str, context_text: str = "") -> str:
    prompt = _with_context(
        f"You are a helpful teacher creating study notes for a {grade} student. "
        f"Write clear, well-organized study notes on the topic: '{topic}'. "
        "Use markdown headings and bullet points, with simple language appropriate for "
        "this grade level. End with a short summary.",
        context_text,
    )
    return _generate(prompt, api_key)


def generate_worksheet(topic: str, grade: str, num_questions: int, api_key: str, context_text: str = "") -> str:
    prompt = _with_context(
        f"Create a practice worksheet for a {grade} student on the topic: '{topic}'. "
        f"Include exactly {num_questions} numbered questions of mixed difficulty "
        "(easy, medium, hard). After the questions, add a separate 'Answer Key' section "
        "with the correct answers and brief explanations. Format the whole thing in markdown.",
        context_text,
    )
    return _generate(prompt, api_key)


def generate_study_plan(
    subject: str, grade: str, duration: str, goal: str, api_key: str, context_text: str = ""
) -> str:
    prompt = _with_context(
        f"Create a structured study plan for a {grade} student studying {subject}. "
        f"The plan should span {duration} and help the student achieve this goal: '{goal}'. "
        "Break it down day-by-day (or week-by-week if the duration is long), with specific "
        "topics, tasks, and short revision checkpoints. Format it as a clear markdown table or list.",
        context_text,
    )
    return _generate(prompt, api_key)


def generate_flashcards(topic: str, grade: str, count: int, api_key: str, context_text: str = "") -> list[dict]:
    """Returns a list of {"question": ..., "answer": ...} dicts."""
    prompt = _with_context(
        f"Create exactly {count} flashcards for a {grade} student studying '{topic}'. "
        'Respond ONLY with a JSON array, no other text, in this exact format: '
        '[{"question": "...", "answer": "..."}, ...]',
        context_text,
    )
    raw = _generate(prompt, api_key)
    try:
        cards = _extract_json(raw)
        if isinstance(cards, list) and cards:
            return cards
    except (json.JSONDecodeError, ValueError):
        pass
    return [{"question": "Raw model output (couldn't be parsed as flashcards)", "answer": raw}]
