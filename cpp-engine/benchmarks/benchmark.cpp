#include <iostream>
#include <chrono>
#include "../graph/prerequisite_dag.h"
#include "../ranking/spaced_repetition.h"
#include "../dp/study_knapsack.h"

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "StudyChart AI - C++ Algorithm Engine Benchmark" << std::endl;
    std::cout << "========================================" << std::endl;

    // 1. DAG Benchmark
    studychart::PrerequisiteDAG dag;
    for (int i = 0; i < 500; ++i) {
        dag.add_topic("T" + std::to_string(i), "Topic " + std::to_string(i), 30, 3.5, 0.4);
        if (i > 0) {
            dag.add_prerequisite("T" + std::to_string(i - 1), "T" + std::to_string(i));
        }
    }

    auto start = std::chrono::high_resolution_clock::now();
    auto order = dag.get_topological_order();
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> dag_time = end - start;
    std::cout << "DAG Topological Sort (500 nodes): " << order.size() << " topics sorted in " 
              << dag_time.count() << " ms" << std::endl;

    // 2. Spaced Repetition Benchmark
    start = std::chrono::high_resolution_clock::now();
    studychart::RepetitionItem item{0, 2.5, 0};
    for (int i = 0; i < 100000; ++i) {
        item = studychart::SpacedRepetitionSM2::calculate_next_review(item, 4);
    }
    end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> sm2_time = end - start;
    std::cout << "Spaced Repetition SM-2 (100k calculations) in " 
              << sm2_time.count() << " ms" << std::endl;

    // 3. Knapsack Optimization Benchmark
    std::vector<studychart::StudyCandidate> candidates;
    for (int i = 0; i < 100; ++i) {
        candidates.push_back({"C" + std::to_string(i), "Module " + std::to_string(i), (i % 4 + 1) * 15, (i % 10 + 1) * 10});
    }
    start = std::chrono::high_resolution_clock::now();
    auto plan = studychart::StudyOptimizer::optimize_daily_session(candidates, 180);
    end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> knapsack_time = end - start;
    std::cout << "Study Knapsack Optimizer (100 candidates, 180 mins limit): " 
              << plan.selected_topics.size() << " topics chosen (Total Value: " 
              << plan.total_value_gained << ") in " << knapsack_time.count() << " ms" << std::endl;

    std::cout << "========================================" << std::endl;
    return 0;
}
