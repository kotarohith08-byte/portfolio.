"""
StudyChart AI - AI Study Planner Service.
"""

import json
from datetime import date, timedelta
from typing import Dict, Any, List, Optional
from app.ai.provider import llm_provider
from app.ai.prompts import STUDY_PLAN_SYSTEM_PROMPT
from app.schemas.study_plan import GeneratePlanRequest, StudyPlanCreate, StudyPlanItemCreate
from cpp_engine.cpp_bridge import cpp_engine

class AIStudyPlanner:
    def generate_plan(self, req: GeneratePlanRequest) -> Dict[str, Any]:
        user_prompt = f"""
        Subjects: {', '.join(req.subject_names)}
        Target Exam Date: {req.exam_date}
        Daily Available Study Hours: {req.daily_hours}
        Difficult Topics: {', '.join(req.difficult_topics or ['None specified'])}
        Important High-Yield Topics: {', '.join(req.important_topics or ['None specified'])}
        Preferred Study Time: {req.preferred_study_time}
        Learning Style: {req.learning_style}
        """

        raw_resp = llm_provider.generate_completion(STUDY_PLAN_SYSTEM_PROMPT, user_prompt)
        try:
            # Clean possible markdown wrapping ```json ... ```
            cleaned = raw_resp.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
            return data
        except Exception:
            # Fallback guarantee
            return {
                "title": f"Study Plan for {', '.join(req.subject_names[:2])}",
                "strategy_overview": "Structured daily focus blocks with spaced repetition and active recall checkpoints.",
                "weekly_hours": req.daily_hours * 6,
                "schedule": [
                    {
                        "day": "Monday",
                        "start_time": "09:00",
                        "end_time": "09:45",
                        "activity_type": "study",
                        "topic": req.subject_names[0] if req.subject_names else "Core Topics",
                        "description": "Fundamental theory and conceptual drill."
                    },
                    {
                        "day": "Monday",
                        "start_time": "10:00",
                        "end_time": "10:45",
                        "activity_type": "practice",
                        "topic": "Practical Exercises",
                        "description": "Problem-solving and scenario application."
                    },
                    {
                        "day": "Monday",
                        "start_time": "18:00",
                        "end_time": "18:30",
                        "activity_type": "revision",
                        "topic": "Daily Review",
                        "description": "Spaced review and flashcards."
                    }
                ],
                "exam_readiness_tips": [
                    "Complete one practice quiz every 2 days.",
                    "Spend more time on difficult topics early in the week."
                ]
            }

ai_study_planner = AIStudyPlanner()
