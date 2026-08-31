#ifndef STUDYCHART_SPACED_REPETITION_H
#define STUDYCHART_SPACED_REPETITION_H

namespace studychart {

struct RepetitionItem {
    int repetitions;      // number of consecutive correct reviews
    double ease_factor;   // SM-2 Easiness factor (default: 2.5, min: 1.3)
    int interval_days;    // Interval until next review in days
};

class SpacedRepetitionSM2 {
public:
    // Quality rating: 0 to 5
    // 5 - perfect response
    // 4 - correct response after hesitation
    // 3 - correct response with serious difficulty
    // 2 - incorrect response; where the correct one seemed easy to recall
    // 1 - incorrect response; the correct one remembered
    // 0 - complete blackout
    static RepetitionItem calculate_next_review(const RepetitionItem& current, int quality_grade);
};

} // namespace studychart

#endif // STUDYCHART_SPACED_REPETITION_H
