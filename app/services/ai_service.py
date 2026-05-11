import json
import re
import anthropic

from app.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

ONBOARDING_SYSTEM_PROMPT = """You are a friendly AI language coach helping a new student set up their personalized vocabulary learning experience.

Your goal is to gather the following information through natural conversation (3-5 turns max):
1. Their native language
2. The language they want to learn (target language)
3. Their current proficiency level (beginner, intermediate, advanced)
4. Their learning goals or topics of interest (e.g., travel, business, daily conversation, specific topics)

Be warm, encouraging, and concise. Ask one or two things at a time. Once you have all the information,
end your response with a JSON block wrapped in <profile> tags like this:

<profile>
{
  "native_language": "English",
  "target_language": "Spanish",
  "proficiency_level": "beginner",
  "learning_goals": "travel and daily conversation",
  "onboarding_complete": true
}
</profile>

Only include the <profile> tag when you have gathered all necessary information and are ready to finalize."""

FLASHCARD_GENERATION_PROMPT = """You are an expert language teacher. Generate {count} flashcards for learning {target_language}.

Student profile:
- Native language: {native_language}
- Proficiency level: {proficiency_level}
- Topic/goals: {topic}

Return ONLY a valid JSON array with this exact structure:
[
  {{
    "front": "word or phrase in {target_language}",
    "back": "translation in {native_language}",
    "example_sentence": "example sentence using the word in {target_language}",
    "pronunciation": "phonetic pronunciation (IPA or simplified)"
  }}
]

Make cards appropriate for the proficiency level. Ensure variety and practical utility."""


def chat_onboarding(messages: list[dict]) -> tuple[str, dict | None]:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=ONBOARDING_SYSTEM_PROMPT,
        messages=messages,
    )
    content = response.content[0].text
    profile = _extract_profile(content)
    clean_content = re.sub(r"<profile>.*?</profile>", "", content, flags=re.DOTALL).strip()
    return clean_content, profile


def generate_flashcards(
    native_language: str,
    target_language: str,
    proficiency_level: str,
    topic: str,
    count: int = 10,
) -> list[dict]:
    prompt = FLASHCARD_GENERATION_PROMPT.format(
        count=count,
        target_language=target_language,
        native_language=native_language,
        proficiency_level=proficiency_level,
        topic=topic,
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    return json.loads(raw)


def _extract_profile(text: str) -> dict | None:
    match = re.search(r"<profile>(.*?)</profile>", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(1).strip())
    except json.JSONDecodeError:
        return None
