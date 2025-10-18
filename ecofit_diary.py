from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict, Optional

@dataclass
class DiaryEntry:
    day: date
    steps: int
    calories: int
    water_ml: int
    mood: str

    def score(self, goals: Dict[str, int]) -> int:
        score = 0
        if self.steps >= goals.get("steps", 8000):
            score += 2
        elif self.steps >= 0.75 * goals.get("steps", 8000):
            score += 1

        if self.water_ml >= goals.get("water_ml", 2000):
            score += 2
        elif self.water_ml >= 0.75 * goals.get("water_ml", 2000):
            score += 1

        cal_goal = goals.get("calories", 2200)
        if self.calories <= cal_goal:
            score += 2
        elif self.calories <= 1.1 * cal_goal:
            score += 1

        mood_score = {"low": 0, "ok": 1, "great": 2}
        score += mood_score.get(self.mood.lower(), 0)
        return score

@dataclass
class Diary:
    entries: List[DiaryEntry] = field(default_factory=list)
    goals: Dict[str, int] = field(default_factory=lambda: {
        "steps": 8000,
        "water_ml": 2000,
        "calories": 2200
    })

    def add_entry(self, entry: DiaryEntry):
        if entry.steps < 0 or entry.calories < 0 or entry.water_ml < 0:
            raise ValueError("Values cannot be negative")
        for i, e in enumerate(self.entries):
            if e.day == entry.day:
                self.entries[i] = entry
                return
        self.entries.append(entry)

    def summary(self) -> Dict[str, float]:
        if not self.entries:
            return {"count": 0, "avg_steps": 0, "avg_cal": 0, "avg_water": 0, "avg_score": 0}
        total_steps = total_cal = total_water = total_score = 0
        for e in self.entries:
            total_steps += e.steps
            total_cal += e.calories
            total_water += e.water_ml
            total_score += e.score(self.goals)
        n = len(self.entries)
        return {
            "count": n,
            "avg_steps": round(total_steps / n, 2),
            "avg_cal": round(total_cal / n, 2),
            "avg_water": round(total_water / n, 2),
            "avg_score": round(total_score / n, 2)
        }

    def best_days(self, top_n: int = 3):
        return sorted(self.entries, key=lambda e: e.score(self.goals), reverse=True)[:top_n]

    def set_goal(self, goal: str, value: int):
        if value <= 0:
            raise ValueError("Goal must be positive.")
        self.goals[goal] = value

    def compare(self, day_a: date, day_b: date):
        entry_a = next((e for e in self.entries if e.day == day_a), None)
        entry_b = next((e for e in self.entries if e.day == day_b), None)
        if not entry_a or not entry_b:
            raise ValueError("Both days must exist.")
        sa, sb = entry_a.score(self.goals), entry_b.score(self.goals)
        return {"result": 1 if sa > sb else -1 if sb > sa else 0, "a": sa, "b": sb}
