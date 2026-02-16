from pydantic import BaseModel


class KeywordMatch(BaseModel):
    keyword: str
    found: bool
    context: str = ""  # Where it was found or suggestion for adding it


class WeakPhrase(BaseModel):
    original: str
    suggestion: str
    reason: str
    location: str = ""  # Approximate location in resume


class Suggestion(BaseModel):
    category: str  # "impact", "keywords", "structure", "formatting"
    priority: str  # "high", "medium", "low"
    title: str
    description: str


class AnalysisResult(BaseModel):
    overall_score: int  # 0-100
    summary: str
    keyword_matches: list[KeywordMatch]
    weak_phrases: list[WeakPhrase]
    suggestions: list[Suggestion]
    strengths: list[str]
