"""
StudyChart AI - Programming Lab Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class TestCaseSchema(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = None

class ProgrammingProblemResponse(BaseModel):
    id: str
    title: str
    slug: str
    description: str
    difficulty: str
    category: str
    constraints: Optional[str] = None
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    starter_code_py: Optional[str] = None
    starter_code_c: Optional[str] = None
    starter_code_cpp: Optional[str] = None
    sample_test_cases: List[TestCaseSchema] = []
    xp_reward: int

    class Config:
        from_attributes = True

class CodeSubmissionRequest(BaseModel):
    problem_id: str
    language: str = Field(..., description="python | c | cpp")
    code: str = Field(..., min_length=1)

class SubmissionResultResponse(BaseModel):
    id: str
    problem_id: str
    language: str
    status: str # Accepted | Wrong Answer | Time Limit Exceeded | Runtime Error | Compilation Error
    passed_test_cases: int
    total_test_cases: int
    execution_time_ms: float
    memory_used_kb: float
    compiler_output: Optional[str] = None
    xp_earned: int = 0
    created_at: datetime

    class Config:
        from_attributes = True
