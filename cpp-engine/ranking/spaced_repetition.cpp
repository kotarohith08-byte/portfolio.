#include "spaced_repetition.h"
#include <algorithm>
#include <cmath>

namespace studychart {

RepetitionItem SpacedRepetitionSM2::calculate_next_review(const RepetitionItem& current, int quality_grade) {
    RepetitionItem next = current;
    if (quality_grade < 0) quality_grade = 0;
    if (quality_grade > 5) quality_grade = 5;

    // Easiness factor calculation: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    double q_diff = 5.0 - quality_grade;
    double new_ef = current.ease_factor + (0.1 - q_diff * (0.08 + q_diff * 0.02));
    if (new_ef < 1.3) new_ef = 1.3;
    next.ease_factor = new_ef;

    if (quality_grade >= 3) {
        if (current.repetitions == 0) {
            next.interval_days = 1;
        } else if (current.repetitions == 1) {
            next.interval_days = 6;
        } else {
            next.interval_days = (int)std::round(current.interval_days * new_ef);
        }
        next.repetitions = current.repetitions + 1;
    } else {
        // Failed attempt: restart repetition sequence
        next.repetitions = 0;
        next.interval_days = 1;
    }

    return next;
}

} // namespace studychart
