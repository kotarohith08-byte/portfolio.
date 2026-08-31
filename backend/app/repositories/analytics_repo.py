"""
StudyChart AI - Analytics Repository.
Executes real SQL aggregations and metrics for user dashboard and analytics.
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta, date
from sqlalchemy import func, distinct
from sqlalchemy.orm import Session
from app.models.study_session import StudySession
from app.models.quiz import QuizAttempt, Quiz, QuizQuestion, QuizAnswer
from app.models.subject import Subject, Topic, Unit
from app.models.user import Profile

class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_metrics(self, user_id: str) -> Dict[str, Any]:
        profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        daily_goal = profile.daily_study_goal_minutes if profile else 120

        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # Today's study time in minutes
        today_study_mins = self.db.query(func.coalesce(func.sum(StudySession.duration_minutes), 0)).filter(
            StudySession.user_id == user_id,
            StudySession.start_time >= today_start,
            StudySession.start_time < today_end
        ).scalar() or 0

        # Total lifetime study minutes and sessions
        total_stats = self.db.query(
            func.coalesce(func.sum(StudySession.duration_minutes), 0),
            func.count(StudySession.id)
        ).filter(StudySession.user_id == user_id).first()

        total_study_mins = total_stats[0] or 0
        total_sessions_count = total_stats[1] or 0

        # Average Quiz Score
        avg_quiz_score = self.db.query(
            func.coalesce(func.avg(QuizAttempt.score), 0.0)
        ).filter(QuizAttempt.user_id == user_id).scalar() or 0.0

        # Weekly study time by day (Last 7 days)
        now = datetime.utcnow()
        weekly_points = []
        for i in range(6, -1, -1):
            d = (now - timedelta(days=i)).date()
            day_name = d.strftime("%a")
            d_start = datetime(d.year, d.month, d.day, 0, 0, 0)
            d_end = d_start + timedelta(days=1)

            day_mins = self.db.query(func.coalesce(func.sum(StudySession.duration_minutes), 0)).filter(
                StudySession.user_id == user_id,
                StudySession.start_time >= d_start,
                StudySession.start_time < d_end
            ).scalar() or 0

            weekly_points.append({"day": day_name, "minutes": int(day_mins)})

        # Subject Progress
        subjects = self.db.query(Subject).filter(
            Subject.user_id == user_id,
            Subject.is_archived == False
        ).all()

        subject_progress_list = []
        for s in subjects:
            subj_mins = self.db.query(func.coalesce(func.sum(StudySession.duration_minutes), 0)).filter(
                StudySession.user_id == user_id,
                StudySession.subject_id == s.id
            ).scalar() or 0

            total_topics = 0
            completed_topics = 0
            for u in s.units:
                total_topics += len(u.topics)
                completed_topics += sum(1 for t in u.topics if t.is_completed)

            pct = (completed_topics / total_topics * 100.0) if total_topics > 0 else 0.0
            subject_progress_list.append({
                "subject_id": s.id,
                "subject_name": s.name,
                "color": s.color,
                "icon": s.icon,
                "total_minutes": int(subj_mins),
                "completion_percentage": round(pct, 1),
                "mastery_score": round(pct, 1)
            })

        # Recent Quizzes
        recent_attempts = self.db.query(QuizAttempt).filter(
            QuizAttempt.user_id == user_id
        ).order_by(QuizAttempt.created_at.desc()).limit(5).all()

        recent_quiz_data = []
        for att in recent_attempts:
            created_str = att.created_at.isoformat() if hasattr(att.created_at, "isoformat") else str(att.created_at)
            recent_quiz_data.append({
                "id": att.id,
                "quiz_id": att.quiz_id,
                "quiz_title": att.quiz.title if att.quiz else "Quiz",
                "score": att.score,
                "correct_count": att.correct_count,
                "total_count": att.total_count,
                "created_at": created_str
            })

        # Calculate Streak
        streak = self.calculate_streak(user_id)
        if profile and profile.current_streak_days != streak:
            profile.current_streak_days = streak
            if streak > profile.longest_streak_days:
                profile.longest_streak_days = streak
            self.db.commit()

        # Weak and Strong topics
        weak_topics, strong_topics = self.get_topic_insights(user_id)

        # AI Insights & Recommendations
        insight = "Great consistency! Keep pushing toward your weekly target."
        recs = [
            "Review your most challenging topics for 30 minutes today.",
            "Take a short 5-question quiz to test active recall.",
            "Complete a Pomodoro session on your priority subject."
        ]

        if weak_topics:
            insight = f"You are making solid progress, but accuracy on '{weak_topics[0]}' needs a quick boost."
            recs = [
                f"Practice 10 review questions on {weak_topics[0]}.",
                f"Review summary notes for {weak_topics[0]}.",
                "Schedule a 45-minute focused session before exam revision."
            ]

        progress_pct = min(100.0, (today_study_mins / daily_goal * 100.0)) if daily_goal > 0 else 0.0

        return {
            "today_goal_minutes": daily_goal,
            "today_completed_minutes": int(today_study_mins),
            "today_progress_percentage": round(progress_pct, 1),
            "current_streak_days": streak,
            "longest_streak_days": profile.longest_streak_days if profile else streak,
            "total_study_minutes": int(total_study_mins),
            "total_study_hours": round(total_study_mins / 60.0, 1),
            "total_sessions_count": total_sessions_count,
            "average_quiz_score": round(float(avg_quiz_score), 1),
            "weekly_study_data": weekly_points,
            "subject_progress": subject_progress_list,
            "recent_quiz_scores": recent_quiz_data,
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "ai_insight": insight,
            "recommended_actions": recs
        }

    def calculate_streak(self, user_id: str) -> int:
        sessions = self.db.query(StudySession.start_time).filter(
            StudySession.user_id == user_id
        ).order_by(StudySession.start_time.desc()).all()

        if not sessions:
            return 0

        dates_set = set()
        for s in sessions:
            st = s[0]
            if st is not None:
                if isinstance(st, datetime):
                    dates_set.add(st.date())
                elif isinstance(st, date):
                    dates_set.add(st)
                elif isinstance(st, str):
                    try:
                        dates_set.add(datetime.strptime(st[:10], "%Y-%m-%d").date())
                    except Exception:
                        pass

        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)

        current_check = today if today in dates_set else yesterday
        if current_check not in dates_set:
            return 0

        streak = 0
        while current_check in dates_set:
            streak += 1
            current_check -= timedelta(days=1)

        return streak

    def get_topic_insights(self, user_id: str) -> Tuple[List[str], List[str]]:
        attempts = self.db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
        topic_scores: Dict[str, List[float]] = {}

        for att in attempts:
            if att.quiz and att.quiz.topic:
                t = att.quiz.topic
                if t not in topic_scores:
                    topic_scores[t] = []
                topic_scores[t].append(att.score)

        weak = []
        strong = []
        for t, scores in topic_scores.items():
            avg = sum(scores) / len(scores)
            if avg < 70.0:
                weak.append(t)
            elif avg >= 85.0:
                strong.append(t)

        return weak, strong
