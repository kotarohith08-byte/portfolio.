#ifndef STUDYCHART_PREREQUISITE_DAG_H
#define STUDYCHART_PREREQUISITE_DAG_H

#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>

namespace studychart {

struct TopicNode {
    std::string id;
    std::string title;
    int estimated_minutes;
    double difficulty; // 1.0 to 5.0
    double current_mastery; // 0.0 to 1.0
};

class PrerequisiteDAG {
private:
    std::unordered_map<std::string, TopicNode> nodes;
    std::unordered_map<std::string, std::vector<std::string>> adj;
    std::unordered_map<std::string, int> in_degree;

public:
    PrerequisiteDAG() = default;

    void add_topic(const std::string& id, const std::string& title, int minutes, double difficulty, double mastery);
    bool add_prerequisite(const std::string& from_id, const std::string& to_id);
    
    // Returns topologically sorted list of topic IDs for optimal study roadmap
    std::vector<std::string> get_topological_order() const;

    // Checks if adding an edge would create a cycle
    bool has_cycle() const;

    // Calculates priority score based on prerequisites, difficulty, and mastery
    std::vector<std::pair<std::string, double>> rank_topics_by_priority() const;
};

} // namespace studychart

#endif // STUDYCHART_PREREQUISITE_DAG_H
