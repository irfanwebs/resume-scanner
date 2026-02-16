import json
from collections.abc import AsyncGenerator

import anthropic

from app.config import get_settings

SYSTEM_PROMPT = """You are an expert resume reviewer and career coach. You analyse resumes against job descriptions to provide actionable, specific feedback.

You MUST respond with valid JSON matching this exact structure:
{
  "overall_score": <number 0-100>,
  "summary": "<2-3 sentence overview of the resume's fit for this role>",
  "keyword_matches": [
    {"keyword": "<term from JD>", "found": <true/false>, "context": "<where found or how to add>"}
  ],
  "weak_phrases": [
    {"original": "<exact phrase from resume>", "suggestion": "<stronger alternative>", "reason": "<why it's weak>", "location": "<section of resume>"}
  ],
  "suggestions": [
    {"category": "<impact|keywords|structure|formatting>", "priority": "<high|medium|low>", "title": "<short title>", "description": "<actionable advice>"}
  ],
  "strengths": ["<specific strength 1>", "<specific strength 2>"]
}

Guidelines:
- Focus on the TOP 8-12 most important keywords from the JD
- Identify 3-5 weak phrases (vague language, passive voice, missing metrics)
- Provide 4-6 prioritised suggestions
- Highlight 2-4 genuine strengths
- Be specific and actionable, not generic
- Score reflects realistic fit: 80+ is strong, 60-79 needs work, below 60 is a significant gap"""


async def analyse_resume(
    resume_text: str,
    job_description: str,
) -> AsyncGenerator[str, None]:
    """Stream AI analysis of resume against job description."""
    settings = get_settings()
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_message = f"""Analyse this resume against the job description below.

---RESUME START---
{resume_text}
---RESUME END---

---JOB DESCRIPTION START---
{job_description}
---JOB DESCRIPTION END---

Respond ONLY with the JSON object. No markdown, no code fences, no explanation."""

    async with client.messages.stream(
        model=settings.model_name,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        async for text in stream.text_stream:
            yield text


async def analyse_resume_full(
    resume_text: str,
    job_description: str,
) -> dict:
    """Get complete AI analysis (non-streaming)."""
    chunks: list[str] = []
    async for chunk in analyse_resume(resume_text, job_description):
        chunks.append(chunk)

    raw = "".join(chunks).strip()

    # Handle potential markdown code fences
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]

    return json.loads(raw)
