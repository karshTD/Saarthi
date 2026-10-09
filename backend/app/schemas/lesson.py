"""The lesson-plan contract shared by the AI generator, the template fallback and the UI."""
from typing import Literal

from pydantic import BaseModel, Field, model_validator

LEVELS = ("struggling", "on_track", "advanced")
Level = Literal["struggling", "on_track", "advanced"]


class LessonSection(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    minutes: int = Field(ge=1, le=240)
    description: str = Field(min_length=1, max_length=1000)


class LessonActivity(BaseModel):
    level: Level
    title: str = Field(min_length=1, max_length=160)
    prompt: str = Field(min_length=1, max_length=1500)
    answer: str | None = Field(default=None, max_length=500)
    materials: list[str] = Field(default_factory=list)


class LessonPlan(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    objective: str = Field(min_length=1, max_length=600)
    total_minutes: int = Field(ge=1, le=240)
    sections: list[LessonSection] = Field(min_length=1)
    activities: list[LessonActivity]
    materials: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)  # filled by retrieval in a later phase

    @model_validator(mode="after")
    def _check_consistency(self) -> "LessonPlan":
        if sum(s.minutes for s in self.sections) != self.total_minutes:
            raise ValueError("section minutes must add up to total_minutes")
        if sorted(a.level for a in self.activities) != sorted(LEVELS):
            raise ValueError("exactly one activity per level is required")
        return self
