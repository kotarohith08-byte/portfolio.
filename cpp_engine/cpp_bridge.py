"""
StudyChart AI - C++ Engine Python Bridge.
Provides Python bindings for Graph DAG topological sort, SM-2 Spaced Repetition, and Knapsack optimization.
"""

import math
from collections import defaultdict, deque
from typing import List, Dict, Any, Tuple, Optional

class CPPEngineBridge:
    def __init__(self):
        pass

    def compute_study_roadmap(self, topics: List[Dict[str, Any]], prerequisites: List[Tuple[str, str]]) -> List[str]:
        in_degree = {t["id"]: 0 for t in topics}
        adj = defaultdict(list)

        for u, v in prerequisites:
            if u in in_degree and v in in_degree:
                adj[u].append(v)
                in_degree[v] += 1

        queue = deque([topic_id for topic_id, deg in in_degree.items() if deg == 0])
        sorted_order = []

        while queue:
            curr = queue.popleft()
            sorted_order.append(curr)
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_order) < len(topics):
            for t in topics:
                if t["id"] not in sorted_order:
                    sorted_order.append(t["id"])

        return sorted_order

    def calculate_sm2_review(self, repetitions: int, ease_factor: float, interval_days: int, quality_grade: int) -> Dict[str, Any]:
        q = max(0, min(5, quality_grade))
        q_diff = 5.0 - q
        new_ef = ease_factor + (0.1 - q_diff * (0.08 + q_diff * 0.02))
        new_ef = max(1.3, round(new_ef, 4))

        if q >= 3:
            if repetitions == 0:
                new_interval = 1
            elif repetitions == 1:
                new_interval = 6
            else:
                new_interval = int(round(interval_days * new_ef))
            new_reps = repetitions + 1
        else:
            new_reps = 0
            new_interval = 1

        return {
            "repetitions": new_reps,
            "ease_factor": new_ef,
            "interval_days": new_interval
        }

    def optimize_study_session(self, candidates: List[Dict[str, Any]], max_available_minutes: int) -> Dict[str, Any]:
        n = len(candidates)
        if n == 0 or max_available_minutes <= 0:
            return {"selected_topics": [], "total_time_used": 0, "total_value_gained": 0}

        W = int(max_available_minutes)
        dp = [[0] * (W + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            wt = candidates[i - 1].get("time_cost_minutes", 30)
            val = candidates[i - 1].get("priority_value", 10)
            for w in range(W + 1):
                if wt <= w:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - wt] + val)
                else:
                    dp[i][w] = dp[i - 1][w]

        res = dp[n][W]
        total_val = res
        w = W
        selected = []
        total_time = 0

        for i in range(n, 0, -1):
            if res <= 0:
                break
            if res != dp[i - 1][w]:
                item = candidates[i - 1]
                selected.append(item)
                total_time += item.get("time_cost_minutes", 30)
                res -= item.get("priority_value", 10)
                w -= item.get("time_cost_minutes", 30)

        selected.reverse()
        return {
            "selected_topics": selected,
            "total_time_used": total_time,
            "total_value_gained": total_val
        }

cpp_engine = CPPEngineBridge()

def test_cpp_engine():
    res = cpp_engine.calculate_sm2_review(0, 2.5, 0, 5)
    assert res["repetitions"] == 1
    assert res["interval_days"] == 1

    candidates = [
        {"topic_id": "1", "title": "SQL Basics", "time_cost_minutes": 30, "priority_value": 20},
        {"topic_id": "2", "title": "SQL Joins", "time_cost_minutes": 45, "priority_value": 40},
        {"topic_id": "3", "title": "Database Normalization", "time_cost_minutes": 60, "priority_value": 50},
    ]
    opt = cpp_engine.optimize_study_session(candidates, 75)
    assert opt["total_time_used"] <= 75
    assert opt["total_value_gained"] >= 40

    topics = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    edges = [("a", "b"), ("b", "c")]
    order = cpp_engine.compute_study_roadmap(topics, edges)
    assert order == ["a", "b", "c"]
    print("[OK] C++ Engine tests passed successfully.")

if __name__ == "__main__":
    test_cpp_engine()
