"""
02. AI Productivity: Automated Task Prioritization & Meeting Notes Extractor
Simulates workflow automation using heuristic scoring (Eisenhower Matrix) and action item extraction.
"""

import re
from dataclasses import dataclass

@dataclass
class Task:
    title: str
    urgency: int      # 1 to 10
    importance: int   # 1 to 10
    effort_hours: float

    @property
    def priority_score(self) -> float:
        return round((self.importance * 2.0 + self.urgency * 1.5) / max(self.effort_hours, 0.5), 2)

    @property
    def quadrant(self) -> str:
        if self.urgency >= 6 and self.importance >= 6:
            return "Q1: Do First"
        elif self.urgency < 6 and self.importance >= 6:
            return "Q2: Schedule"
        elif self.urgency >= 6 and self.importance < 6:
            return "Q3: Delegate"
        return "Q4: Eliminate / Defer"

def extract_action_items(transcript: str) -> list[dict]:
    """Extracts action items from raw meeting notes using pattern matching."""
    pattern = r"(?:TODO|ACTION|ASSIGNED):\s*([A-Za-z]+)\s*-\s*(.+)"
    matches = re.findall(pattern, transcript, flags=re.IGNORECASE)
    return [{"owner": owner.strip(), "task": task.strip()} for owner, task in matches]

if __name__ == "__main__":
    tasks = [
        Task("Deploy critical security patch", urgency=9, importance=10, effort_hours=2.0),
        Task("Design Q4 architecture roadmap", urgency=4, importance=9, effort_hours=5.0),
        Task("Update internal wiki formatting", urgency=3, importance=2, effort_hours=1.5),
        Task("Respond to client status email", urgency=8, importance=5, effort_hours=0.5),
    ]

    print("=== AI Productivity: Smart Task Prioritizer ===")
    for t in sorted(tasks, key=lambda x: x.priority_score, reverse=True):
        print(f"[{t.quadrant}] {t.title} (Score: {t.priority_score}, Effort: {t.effort_hours}h)")

    sample_notes = """
    Sprint Sync Notes:
    We reviewed the backend latency metrics.
    ACTION: Alex - Optimize database indexing on user_events table by Friday.
    TODO: Priya - Prepare benchmark report for the new embedding model.
    ASSIGNED: Sam - Update CI/CD pipeline configuration.
    """
    print("\n=== Extracted Action Items ===")
    for item in extract_action_items(sample_notes):
        print(f"Owner: {item['owner']} | Task: {item['task']}")
