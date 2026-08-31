#include "stats.h"
#include <stdlib.h>
#include <math.h>
#include <string.h>

static int compare_doubles(const void* a, const void* b) {
    double diff = (*(double*)a - *(double*)b);
    if (diff < 0) return -1;
    if (diff > 0) return 1;
    return 0;
}

double calculate_mean(const double* data, int size) {
    if (data == NULL || size <= 0) return 0.0;
    double sum = 0.0;
    for (int i = 0; i < size; ++i) {
        sum += data[i];
    }
    return sum / (double)size;
}

double calculate_variance(const double* data, int size) {
    if (data == NULL || size <= 1) return 0.0;
    double mean = calculate_mean(data, size);
    double sum_sq_diff = 0.0;
    for (int i = 0; i < size; ++i) {
        double diff = data[i] - mean;
        sum_sq_diff += diff * diff;
    }
    return sum_sq_diff / (double)(size - 1);
}

double calculate_std_dev(const double* data, int size) {
    return sqrt(calculate_variance(data, size));
}

double calculate_percentile(double* data, int size, double p) {
    if (data == NULL || size <= 0 || p < 0.0 || p > 100.0) return 0.0;
    double* sorted = (double*)malloc(size * sizeof(double));
    if (sorted == NULL) return 0.0;
    memcpy(sorted, data, size * sizeof(double));
    qsort(sorted, size, sizeof(double), compare_doubles);

    double index = (p / 100.0) * (size - 1);
    int lower = (int)floor(index);
    int upper = (int)ceil(index);
    double weight = index - lower;

    double result = (1.0 - weight) * sorted[lower] + weight * sorted[upper];
    free(sorted);
    return result;
}

void calculate_descriptive_stats(const double* data, int size, DescriptiveStats* result) {
    if (result == NULL) return;
    if (data == NULL || size <= 0) {
        result->mean = 0.0;
        result->variance = 0.0;
        result->std_dev = 0.0;
        result->min = 0.0;
        result->max = 0.0;
        result->median = 0.0;
        return;
    }

    result->mean = calculate_mean(data, size);
    result->variance = calculate_variance(data, size);
    result->std_dev = sqrt(result->variance);

    double min_val = data[0];
    double max_val = data[0];
    for (int i = 1; i < size; ++i) {
        if (data[i] < min_val) min_val = data[i];
        if (data[i] > max_val) max_val = data[i];
    }
    result->min = min_val;
    result->max = max_val;

    double* sorted = (double*)malloc(size * sizeof(double));
    if (sorted != NULL) {
        memcpy(sorted, data, size * sizeof(double));
        qsort(sorted, size, sizeof(double), compare_doubles);
        if (size % 2 == 0) {
            result->median = (sorted[size / 2 - 1] + sorted[size / 2]) / 2.0;
        } else {
            result->median = sorted[size / 2];
        }
        free(sorted);
    } else {
        result->median = result->mean;
    }
}

void calculate_exponential_moving_average(const double* data, int size, double alpha, double* output) {
    if (data == NULL || output == NULL || size <= 0) return;
    if (alpha <= 0.0 || alpha > 1.0) alpha = 0.3;

    output[0] = data[0];
    for (int i = 1; i < size; ++i) {
        output[i] = alpha * data[i] + (1.0 - alpha) * output[i - 1];
    }
}

void calculate_linear_regression(const double* x, const double* y, int size, LinearRegressionResult* result) {
    if (result == NULL) return;
    result->slope = 0.0;
    result->intercept = 0.0;
    result->r_squared = 0.0;

    if (x == NULL || y == NULL || size <= 1) return;

    double x_mean = calculate_mean(x, size);
    double y_mean = calculate_mean(y, size);

    double numerator = 0.0;
    double denom_x = 0.0;
    double denom_y = 0.0;

    for (int i = 0; i < size; ++i) {
        double x_diff = x[i] - x_mean;
        double y_diff = y[i] - y_mean;
        numerator += x_diff * y_diff;
        denom_x += x_diff * x_diff;
        denom_y += y_diff * y_diff;
    }

    if (denom_x != 0.0) {
        result->slope = numerator / denom_x;
        result->intercept = y_mean - result->slope * x_mean;
    }

    if (denom_x > 0.0 && denom_y > 0.0) {
        double r = numerator / sqrt(denom_x * denom_y);
        result->r_squared = r * r;
    }
}
