"""
StudyChart AI - AI Conversational Tutor Service.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.ai.provider import llm_provider
from app.ai.prompts import AI_TUTOR_SYSTEM_PROMPT
from app.models.ai_chat import AIConversation, AIMessage
from app.schemas.ai import AITutorMessageRequest, AITutorResponse

class AITutorService:
    def handle_message(self, db: Session, user_id: str, req: AITutorMessageRequest) -> AITutorResponse:
        # Get or create conversation
        if req.conversation_id:
            conv = db.query(AIConversation).filter(
                AIConversation.id == req.conversation_id,
                AIConversation.user_id == user_id
            ).first()
        else:
            conv = None

        if not conv:
            conv = AIConversation(
                user_id=user_id,
                title=req.message[:50] + ("..." if len(req.message) > 50 else ""),
                subject_id=req.subject_id,
                topic=req.topic
            )
            db.add(conv)
            db.flush()

        # Save user message
        user_msg = AIMessage(
            conversation_id=conv.id,
            role="user",
            content=req.message,
            tokens_used=len(req.message.split())
        )
        db.add(user_msg)

        # Build context from past messages (last 6 messages)
        past_msgs = db.query(AIMessage).filter(
            AIMessage.conversation_id == conv.id
        ).order_by(AIMessage.created_at.desc()).limit(6).all()

        history_context = "\n".join([f"{m.role.upper()}: {m.content}" for m in reversed(past_msgs)])
        custom_system_prompt = f"{AI_TUTOR_SYSTEM_PROMPT}\nTarget Student Level: {req.difficulty_level}\n"
        full_user_prompt = f"Chat History:\n{history_context}\n\nUSER QUESTION: {req.message}"

        # Generate response
        assistant_reply = llm_provider.generate_completion(custom_system_prompt, full_user_prompt)

        # Save assistant message
        ai_msg = AIMessage(
            conversation_id=conv.id,
            role="assistant",
            content=assistant_reply,
            tokens_used=len(assistant_reply.split())
        )
        db.add(ai_msg)
        db.commit()

        # Generate follow-up suggestions
        followups = [
            "Explain with another practical example",
            "Generate a 3-question quiz on this topic",
            "What are the common edge cases to watch out for?"
        ]

        return AITutorResponse(
            conversation_id=conv.id,
            message=assistant_reply,
            suggested_followups=followups
        )

ai_tutor = AITutorService()
