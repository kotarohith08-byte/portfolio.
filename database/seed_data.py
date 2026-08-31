"""
StudyChart AI - Database Seeder.
Populates standard achievements, sample computer science subjects, and coding problems for development and demo accounts.
"""

import sys
import os
import json

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.database.session import SessionLocal, engine
from app.database.base import Base
import app.models
from app.models.achievement import Achievement
from app.models.programming import ProgrammingProblem

def seed_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("Seeding achievements...")
        achievements_data = [
            {
                "code": "first_session",
                "title": "First Step",
                "description": "Logged your first study session in StudyChart AI.",
                "icon": "zap",
                "category": "study",
                "xp_reward": 50,
                "requirement_type": "sessions_count",
                "requirement_target": 1
            },
            {
                "code": "streak_7",
                "title": "7-Day Consistency Master",
                "description": "Maintained an unbroken 7-day study streak.",
                "icon": "flame",
                "category": "streak",
                "xp_reward": 150,
                "requirement_type": "streak_days",
                "requirement_target": 7
            },
            {
                "code": "streak_30",
                "title": "Unstoppable Scholar",
                "description": "Maintained an unbroken 30-day study streak.",
                "icon": "award",
                "category": "streak",
                "xp_reward": 500,
                "requirement_type": "streak_days",
                "requirement_target": 30
            },
            {
                "code": "hours_10",
                "title": "Dedicated Learner",
                "description": "Completed 10 hours of active focused study.",
                "icon": "clock",
                "category": "study_time",
                "xp_reward": 200,
                "requirement_type": "study_hours",
                "requirement_target": 10
            },
            {
                "code": "hours_50",
                "title": "Deep Work Master",
                "description": "Completed 50 hours of active focused study.",
                "icon": "shield",
                "category": "study_time",
                "xp_reward": 600,
                "requirement_type": "study_hours",
                "requirement_target": 50
            },
            {
                "code": "first_quiz",
                "title": "Knowledge Seeker",
                "description": "Completed your first active recall quiz.",
                "icon": "help-circle",
                "category": "quiz",
                "xp_reward": 50,
                "requirement_type": "quiz_count",
                "requirement_target": 1
            },
            {
                "code": "quiz_10",
                "title": "Quiz Veteran",
                "description": "Completed 10 AI diagnostic quizzes.",
                "icon": "check-circle",
                "category": "quiz",
                "xp_reward": 250,
                "requirement_type": "quiz_count",
                "requirement_target": 10
            },
            {
                "code": "quiz_master_90",
                "title": "High Honors",
                "description": "Scored 90% or above on a diagnostic quiz.",
                "icon": "star",
                "category": "quiz",
                "xp_reward": 100,
                "requirement_type": "quiz_score",
                "requirement_target": 90
            },
            {
                "code": "first_problem",
                "title": "Hello, World!",
                "description": "Solved your first programming challenge.",
                "icon": "code",
                "category": "coding",
                "xp_reward": 75,
                "requirement_type": "code_count",
                "requirement_target": 1
            }
        ]

        for ach in achievements_data:
            existing = db.query(Achievement).filter(Achievement.code == ach["code"]).first()
            if not existing:
                db.add(Achievement(**ach))

        print("Seeding programming problems...")
        problems_data = [
            {
                "title": "Two Sum Target",
                "slug": "two-sum-target",
                "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\nAssume each input has exactly one solution.",
                "difficulty": "Easy",
                "category": "Algorithms",
                "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9",
                "input_format": "Line 1: Comma-separated integers\nLine 2: Target integer",
                "output_format": "Two space-separated indices",
                "starter_code_py": "def two_sum(nums, target):\n    # Write your solution here\n    pass\n\nimport sys\nlines = sys.stdin.read().strip().split('\\n')\nif len(lines) >= 2:\n    nums = [int(x.strip()) for x in lines[0].split(',')]\n    target = int(lines[1].strip())\n    seen = {}\n    for i, n in enumerate(nums):\n        diff = target - n\n        if diff in seen:\n            print(f\"{seen[diff]} {i}\")\n            break\n        seen[n] = i\n",
                "starter_code_c": "#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    // Solve Two Sum\n    printf(\"0 1\\n\");\n    return 0;\n}",
                "starter_code_cpp": "#include <iostream>\n#include <vector>\n#include <unordered_map>\n\nint main() {\n    // Solve Two Sum\n    std::cout << \"0 1\" << std::endl;\n    return 0;\n}",
                "sample_test_cases_json": json.dumps([
                    {"input": "2,7,11,15\n9", "output": "0 1", "explanation": "nums[0] + nums[1] == 9, so we output 0 1"}
                ]),
                "hidden_test_cases_json": json.dumps([
                    {"input": "3,2,4\n6", "output": "1 2"},
                    {"input": "3,3\n6", "output": "0 1"}
                ]),
                "xp_reward": 30
            },
            {
                "title": "Reverse String in-place",
                "slug": "reverse-string",
                "description": "Write a program that takes a string input and prints the reversed string without allocating additional array buffers.",
                "difficulty": "Easy",
                "category": "Data Structures",
                "constraints": "1 <= s.length <= 10^5",
                "input_format": "A single line containing the string",
                "output_format": "Reversed string",
                "starter_code_py": "import sys\ns = sys.stdin.read().strip()\nprint(s[::-1])\n",
                "starter_code_c": "#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[1000];\n    if (scanf(\"%s\", s) == 1) {\n        int len = strlen(s);\n        for (int i = len - 1; i >= 0; i--) putchar(s[i]);\n        putchar('\\n');\n    }\n    return 0;\n}",
                "starter_code_cpp": "#include <iostream>\n#include <string>\n#include <algorithm>\n\nint main() {\n    std::string s;\n    if (std::cin >> s) {\n        std::reverse(s.begin(), s.end());\n        std::cout << s << std::endl;\n    }\n    return 0;\n}",
                "sample_test_cases_json": json.dumps([
                    {"input": "hello", "output": "olleh"}
                ]),
                "hidden_test_cases_json": json.dumps([
                    {"input": "studychart", "output": "trahcychduts"},
                    {"input": "algorithm", "output": "mhtirogla"}
                ]),
                "xp_reward": 25
            },
            {
                "title": "Valid Parentheses Matcher",
                "slug": "valid-parentheses",
                "description": "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\nAn input string is valid if open brackets are closed by the same type of brackets in correct order.",
                "difficulty": "Medium",
                "category": "Algorithms",
                "constraints": "1 <= s.length <= 10^4",
                "input_format": "A single line string",
                "output_format": "true or false",
                "starter_code_py": "import sys\ndef is_valid(s):\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n\ns = sys.stdin.read().strip()\nprint('true' if is_valid(s) else 'false')\n",
                "starter_code_c": "#include <stdio.h>\nint main() {\n    printf(\"true\\n\");\n    return 0;\n}",
                "starter_code_cpp": "#include <iostream>\nint main() {\n    std::cout << \"true\" << std::endl;\n    return 0;\n}",
                "sample_test_cases_json": json.dumps([
                    {"input": "()[]{}", "output": "true"},
                    {"input": "(]", "output": "false"}
                ]),
                "hidden_test_cases_json": json.dumps([
                    {"input": "([)]", "output": "false"},
                    {"input": "{[]}", "output": "true"}
                ]),
                "xp_reward": 45
            }
        ]

        for prob in problems_data:
            existing = db.query(ProgrammingProblem).filter(ProgrammingProblem.slug == prob["slug"]).first()
            if not existing:
                db.add(ProgrammingProblem(**prob))

        db.commit()
        print("Database seeded successfully with achievements and coding problems!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
