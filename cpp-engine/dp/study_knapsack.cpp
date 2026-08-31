#include "study_knapsack.h"
#include <vector>
#include <algorithm>

namespace studychart {

KnapsackPlan StudyOptimizer::optimize_daily_session(
    const std::vector<StudyCandidate>& candidates,
    int max_available_minutes
) {
    KnapsackPlan plan{ {}, 0, 0 };
    int n = (int)candidates.size();
    if (n == 0 || max_available_minutes <= 0) return plan;

    // dp[i][w] represents max value considering first i items with weight w
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(max_available_minutes + 1, 0));

    for (int i = 1; i <= n; ++i) {
        int wt = candidates[i - 1].time_cost_minutes;
        int val = candidates[i - 1].priority_value;
        for (int w = 0; w <= max_available_minutes; ++w) {
            if (wt <= w) {
                dp[i][w] = std::max(dp[i - 1][w], dp[i - 1][w - wt] + val);
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    // Backtrack to find selected items
    int res = dp[n][max_available_minutes];
    plan.total_value_gained = res;
    int w = max_available_minutes;

    for (int i = n; i > 0 && res > 0; --i) {
        if (res != dp[i - 1][w]) {
            plan.selected_topics.push_back(candidates[i - 1]);
            plan.total_time_used += candidates[i - 1].time_cost_minutes;
            res -= candidates[i - 1].priority_value;
            w -= candidates[i - 1].time_cost_minutes;
        }
    }

    std::reverse(plan.selected_topics.begin(), plan.selected_topics.end());
    return plan;
}

} // namespace studychart
