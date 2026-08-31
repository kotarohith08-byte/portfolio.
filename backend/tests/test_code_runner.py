"""
StudyChart AI - Sandboxed Code Runner Tests.
"""

from app.services.code_runner import code_runner

def test_python_code_execution_accepted():
    code = "import sys\nline = sys.stdin.read().strip()\nprint(f'Hello, {line}!')\n"
    test_cases = [
        {"input": "StudyChart", "output": "Hello, StudyChart!"}
    ]
    res = code_runner.execute_code("python", code, test_cases)
    assert res["status"] == "Accepted"
    assert res["passed_test_cases"] == 1

def test_python_code_execution_wrong_answer():
    code = "print('Wrong Output')"
    test_cases = [
        {"input": "input", "output": "Expected"}
    ]
    res = code_runner.execute_code("python", code, test_cases)
    assert res["status"] == "Wrong Answer"

def test_dangerous_syscall_blocked():
    code = "import os\nos.system('echo dangerous')"
    test_cases = [{"input": "", "output": ""}]
    res = code_runner.execute_code("python", code, test_cases)
    assert res["status"] == "Runtime Error"
    assert "Unsafe system operation" in res["compiler_output"]
