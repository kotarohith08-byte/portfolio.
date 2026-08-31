#include "prerequisite_dag.h"
#include <queue>
#include <algorithm>

namespace studychart {

void PrerequisiteDAG::add_topic(const std::string& id, const std::string& title, int minutes, double difficulty, double mastery) {
    TopicNode node{id, title, minutes, difficulty, mastery};
    nodes[id] = node;
    if (adj.find(id) == adj.end()) {
        adj[id] = std::vector<std::string>();
    }
    if (in_degree.find(id) == in_degree.end()) {
        in_degree[id] = 0;
    }
}

bool PrerequisiteDAG::add_prerequisite(const std::string& from_id, const std::string& to_id) {
    if (nodes.find(from_id) == nodes.end() || nodes.find(to_id) == nodes.end()) {
        return false;
    }
    adj[from_id].push_back(to_id);
    in_degree[to_id]++;
    return true;
}

bool PrerequisiteDAG::has_cycle() const {
    std::unordered_map<std::string, int> current_in_degree = in_degree;
    std::queue<std::string> q;

    for (const auto& pair : nodes) {
        if (current_in_degree[pair.first] == 0) {
            q.push(pair.first);
        }
    }

    int visited_count = 0;
    while (!q.empty()) {
        std::string curr = q.front();
        q.pop();
        visited_count++;

        auto it = adj.find(curr);
        if (it != adj.end()) {
            for (const std::string& neighbor : it->second) {
                current_in_degree[neighbor]--;
                if (current_in_degree[neighbor] == 0) {
                    q.push(neighbor);
                }
            }
        }
    }

    return visited_count != (int)nodes.size();
}

std::vector<std::string> PrerequisiteDAG::get_topological_order() const {
    std::vector<std::string> order;
    std::unordered_map<std::string, int> current_in_degree = in_degree;
    std::queue<std::string> q;

    for (const auto& pair : nodes) {
        if (current_in_degree[pair.first] == 0) {
            q.push(pair.first);
        }
    }

    while (!q.empty()) {
        std::string curr = q.front();
        q.pop();
        order.push_back(curr);

        auto it = adj.find(curr);
        if (it != adj.end()) {
            for (const std::string& neighbor : it->second) {
                current_in_degree[neighbor]--;
                if (current_in_degree[neighbor] == 0) {
                    q.push(neighbor);
                }
            }
        }
    }

    return order;
}

std::vector<std::pair<std::string, double>> PrerequisiteDAG::rank_topics_by_priority() const {
    std::vector<std::pair<std::string, double>> ranking;
    for (const auto& pair : nodes) {
        const TopicNode& n = pair.second;
        // Priority formula: high difficulty + low mastery + high downstream dependency impact
        int downstream_count = 0;
        auto it = adj.find(n.id);
        if (it != adj.end()) {
            downstream_count = (int)it->second.size();
        }
        double priority = (1.0 - n.current_mastery) * 40.0 + (n.difficulty / 5.0) * 30.0 + (downstream_count * 10.0);
        ranking.push_back({n.id, priority});
    }

    std::sort(ranking.begin(), ranking.end(), [](const auto& a, const auto& b) {
        return a.second > b.second;
    });

    return ranking;
}

} // namespace studychart
