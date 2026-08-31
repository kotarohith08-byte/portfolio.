#ifndef STUDYCHART_STUDY_KNAPSACK_H
#define STUDYCHART_STUDY_KNAPSACK_H

#include <vector>
#include <string>

namespace studychart {

struct StudyCandidate {
    std::string topic_id;
    std::string title;
    int time_cost_minutes; // Weight
    int priority_value;    // Value/Importance
};

struct KnapsackPlan {
    std::vector<StudyCandidate> selected_topics;
    int total_time_used;
    int total_value_gained;
};

class StudyOptimizer {
public:
    static KnapsackPlan optimize_daily_session(
        const std::vector<StudyCandidate>& candidates,
        int max_available_minutes
    );
};

} // namespace studychart

#endif // STUDYCHART_STUDY_KNAPSACK_H
