"""
StudyChart AI - AI Cost Control and Usage Quotas.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.ai_chat import AIUsageLog
from app.core.config import settings
from app.core.errors import RateLimitExceededException

class AICostController:
    def log_and_check_quota(
        self,
        db: Session,
        user_id: str,
        endpoint: str,
        prompt_tokens: int = 150,
        completion_tokens: int = 300,
        model_name: str = "gemini-1.5-flash"
    ) -> None:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        # Count daily AI requests
        daily_count = db.query(func.count(AIUsageLog.id)).filter(
            AIUsageLog.user_id == user_id,
            AIUsageLog.created_at >= today_start
        ).scalar() or 0

        if daily_count >= settings.DAILY_AI_REQUEST_LIMIT:
            raise RateLimitExceededException(
                f"Daily AI request limit ({settings.DAILY_AI_REQUEST_LIMIT} requests/day) reached. Resets at midnight UTC."
            )

        # Estimate cost ($0.0001 per 1k tokens)
        total_tokens = prompt_tokens + completion_tokens
        cost = (total_tokens / 1000.0) * 0.0001

        log_entry = AIUsageLog(
            user_id=user_id,
            endpoint=endpoint,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            estimated_cost_usd=round(cost, 6),
            model_name=model_name
        )
        db.add(log_entry)
        db.commit()

ai_cost_controller = AICostController()
