"""
StudyChart AI - Programming Practice API Endpoints.
"""

import json
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.programming import ProgrammingProblem, CodeSubmission
from app.schemas.programming import (
    ProgrammingProblemResponse,
    CodeSubmissionRequest,
    SubmissionResultResponse,
    TestCaseSchema
)
from app.services.code_runner import code_runner
from app.services.gamification_service import GamificationService
from app.core.errors import ResourceNotFoundException
from app.core.rate_limiter import check_rate_limit

router = APIRouter(prefix="/programming", tags=["Programming Lab"])

def serialize_problem(p: ProgrammingProblem) -> dict:
    sample_tests = []
    if p.sample_test_cases_json:
        try:
            sample_tests = json.loads(p.sample_test_cases_json)
        except Exception:
            pass

    return {
        "id": p.id,
        "title": p.title,
        "slug": p.slug,
        "description": p.description,
        "difficulty": p.difficulty,
        "category": p.category,
        "constraints": p.constraints,
        "input_format": p.input_format,
        "output_format": p.output_format,
        "starter_code_py": p.starter_code_py,
        "starter_code_c": p.starter_code_c,
        "starter_code_cpp": p.starter_code_cpp,
        "sample_test_cases": sample_tests,
        "xp_reward": p.xp_reward
    }

@router.get("/problems", response_model=List[ProgrammingProblemResponse])
def list_problems(db: Session = Depends(get_db)):
    problems = db.query(ProgrammingProblem).order_by(ProgrammingProblem.created_at.asc()).all()
    return [serialize_problem(p) for p in problems]

@router.get("/problems/{slug}", response_model=ProgrammingProblemResponse)
def get_problem_by_slug(slug: str, db: Session = Depends(get_db)):
    problem = db.query(ProgrammingProblem).filter(ProgrammingProblem.slug == slug).first()
    if not problem:
        raise ResourceNotFoundException(f"Problem '{slug}' not found.")
    return serialize_problem(problem)

@router.post("/submit", response_model=SubmissionResultResponse)
def submit_code(
    req: CodeSubmissionRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_rate_limit(request, limit_type="code_exec", max_requests=20, window_seconds=60)

    problem = db.query(ProgrammingProblem).filter(ProgrammingProblem.id == req.problem_id).first()
    if not problem:
        raise ResourceNotFoundException("Problem not found.")

    # Load all test cases
    sample_tc = json.loads(problem.sample_test_cases_json) if problem.sample_test_cases_json else []
    hidden_tc = json.loads(problem.hidden_test_cases_json) if problem.hidden_test_cases_json else []
    all_tests = sample_tc + hidden_tc

    # Execute in sandboxed runner
    result = code_runner.execute_code(
        language=req.language,
        code=req.code,
        test_cases=all_tests
    )

    xp_earned = 0
    if result["status"] == "Accepted":
        xp_earned = problem.xp_reward
        gamify_svc = GamificationService(db)
        gamify_svc.award_xp(current_user.id, xp_earned, f"Solved {problem.title}")

    submission = CodeSubmission(
        user_id=current_user.id,
        problem_id=problem.id,
        language=req.language,
        code=req.code,
        status=result["status"],
        passed_test_cases=result["passed_test_cases"],
        total_test_cases=result["total_test_cases"],
        execution_time_ms=result["execution_time_ms"],
        memory_used_kb=result["memory_used_kb"],
        compiler_output=result["compiler_output"]
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return SubmissionResultResponse(
        id=submission.id,
        problem_id=submission.problem_id,
        language=submission.language,
        status=submission.status,
        passed_test_cases=submission.passed_test_cases,
        total_test_cases=submission.total_test_cases,
        execution_time_ms=submission.execution_time_ms,
        memory_used_kb=submission.memory_used_kb,
        compiler_output=submission.compiler_output,
        xp_earned=xp_earned,
        created_at=submission.created_at
    )
