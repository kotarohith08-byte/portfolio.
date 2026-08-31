"""
StudyChart AI - Centralized Error Handling.
"""

from typing import Any, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class StudyChartException(Exception):
    def __init__(self, message: str, code: str = "BAD_REQUEST", status_code: int = status.HTTP_400_BAD_REQUEST, details: Any = None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

class ResourceNotFoundException(StudyChartException):
    def __init__(self, message: str = "Resource not found.", details: Any = None):
        super().__init__(message=message, code="RESOURCE_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND, details=details)

class UnauthorizedException(StudyChartException):
    def __init__(self, message: str = "Authentication required.", details: Any = None):
        super().__init__(message=message, code="UNAUTHORIZED", status_code=status.HTTP_401_UNAUTHORIZED, details=details)

class ForbiddenException(StudyChartException):
    def __init__(self, message: str = "Access denied to requested resource.", details: Any = None):
        super().__init__(message=message, code="FORBIDDEN", status_code=status.HTTP_403_FORBIDDEN, details=details)

class RateLimitExceededException(StudyChartException):
    def __init__(self, message: str = "Rate limit exceeded. Please wait a moment.", details: Any = None):
        super().__init__(message=message, code="RATE_LIMIT_EXCEEDED", status_code=status.HTTP_429_TOO_MANY_REQUESTS, details=details)

def format_error_response(code: str, message: str, details: Any = None, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details
            }
        }
    )

async def studychart_exception_handler(request: Request, exc: StudyChartException) -> JSONResponse:
    return format_error_response(
        code=exc.code,
        message=exc.message,
        details=exc.details,
        status_code=exc.status_code
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "RESOURCE_NOT_FOUND",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_SERVER_ERROR",
    }
    code = code_map.get(exc.status_code, "ERROR")
    message = exc.detail if isinstance(exc.detail, str) else "An HTTP error occurred."
    return format_error_response(code=code, message=message, status_code=exc.status_code)

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    formatted_errors = []
    for err in exc.errors():
        loc = " -> ".join(str(l) for l in err.get("loc", []))
        msg = err.get("msg", "Invalid value")
        formatted_errors.append(f"{loc}: {msg}")
    return format_error_response(
        code="VALIDATION_ERROR",
        message="Request payload failed validation.",
        details=formatted_errors,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return format_error_response(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected internal server error occurred.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
