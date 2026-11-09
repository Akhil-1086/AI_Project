"""Optional Groq client. Local mode remains available without credentials."""
from config import GROQ_API_KEY, GROQ_MODEL


def generate(prompt: str, system: str = "You are a careful study tutor.") -> str | None:
    if not GROQ_API_KEY:
        return None
    try:
        from groq import Groq
        response = Groq(api_key=GROQ_API_KEY).chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content or ""
    except Exception as exc:
        raise RuntimeError(f"Groq request failed: {exc}") from exc
