"""
StudyChart AI - Programming Problem and Code Submission Models.
"""

from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, UserOwnedMixin

class ProgrammingProblem(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "programming_problems"

    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(50), default="Easy", nullable=False) # Easy | Medium | Hard
    category = Column(String(100), default="Algorithms", nullable=False) # Algorithms | Data Structures | Math | DBMS
    constraints = Column(Text, nullable=True)
    input_format = Column(Text, nullable=True)
    output_format = Column(Text, nullable=True)
    starter_code_py = Column(Text, nullable=True)
    starter_code_c = Column(Text, nullable=True)
    starter_code_cpp = Column(Text, nullable=True)
    sample_test_cases_json = Column(Text, nullable=False) # JSON array of {input: ..., output: ...}
    hidden_test_cases_json = Column(Text, nullable=False) # JSON array of {input: ..., output: ...}
    xp_reward = Column(Integer, default=20, nullable=False)

    submissions = relationship("CodeSubmission", back_populates="problem", cascade="all, delete-orphan")

class CodeSubmission(Base, UUIDPrimaryKeyMixin, TimestampMixin, UserOwnedMixin):
    __tablename__ = "code_submissions"

    problem_id = Column(String(36), ForeignKey("programming_problems.id", ondelete="CASCADE"), nullable=False, index=True)
    language = Column(String(50), nullable=False) # python | c | cpp
    code = Column(Text, nullable=False)
    status = Column(String(50), default="Accepted", nullable=False) # Accepted | Wrong Answer | Time Limit Exceeded | Runtime Error | Compilation Error
    passed_test_cases = Column(Integer, default=0, nullable=False)
    total_test_cases = Column(Integer, default=0, nullable=False)
    execution_time_ms = Column(Float, default=0.0, nullable=False)
    memory_used_kb = Column(Float, default=0.0, nullable=False)
    compiler_output = Column(Text, nullable=True)

    user = relationship("User", back_populates="code_submissions")
    problem = relationship("ProgrammingProblem", back_populates="submissions")
