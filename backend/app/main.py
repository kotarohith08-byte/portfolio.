"""
StudyChart AI - Production FastAPI Main Application.
"""

import os
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.logging import logger
from app.core.errors import (
    StudyChartException,
    studychart_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler
)
from app.database.base import Base
from app.database.session import engine

# Import all models to guarantee registration with Base.metadata
import app.models

# Routers
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.subjects import router as subjects_router
from app.api.v1.study_plans import router as study_plans_router
from app.api.v1.study_sessions import router as study_sessions_router
from app.api.v1.quizzes import router as quizzes_router
from app.api.v1.notes import router as notes_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.ai import router as ai_router
from app.api.v1.calendar import router as calendar_router
from app.api.v1.achievements import router as achievements_router
from app.api.v1.programming import router as programming_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.search import router as search_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent Personal Learning Operating System — AI Study Planning, Adaptive Quizzes, Spaced Repetition, Code Practice, and Performance Analytics.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Centralized Error Handlers
app.add_exception_handler(StudyChartException, studychart_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Include Routers
api_v1 = settings.API_V1_STR
app.include_router(auth_router, prefix=api_v1)
app.include_router(users_router, prefix=api_v1)
app.include_router(subjects_router, prefix=api_v1)
app.include_router(study_plans_router, prefix=api_v1)
app.include_router(study_sessions_router, prefix=api_v1)
app.include_router(quizzes_router, prefix=api_v1)
app.include_router(notes_router, prefix=api_v1)
app.include_router(dashboard_router, prefix=api_v1)
app.include_router(analytics_router, prefix=api_v1)
app.include_router(ai_router, prefix=api_v1)
app.include_router(calendar_router, prefix=api_v1)
app.include_router(achievements_router, prefix=api_v1)
app.include_router(programming_router, prefix=api_v1)
app.include_router(notifications_router, prefix=api_v1)
app.include_router(search_router, prefix=api_v1)

@app.get("/health", tags=["Health"])
def healthcheck():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

# Mount frontend directory for easy serving
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENVIRONMENT}]")
