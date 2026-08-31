#ifndef STUDYCHART_STATS_H
#define STUDYCHART_STATS_H

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _WIN32
  #define EXPORT_API __declspec(dllexport)
#else
  #define EXPORT_API __attribute__((visibility("default")))
#endif

typedef struct {
    double slope;
    double intercept;
    double r_squared;
} LinearRegressionResult;

typedef struct {
    double mean;
    double variance;
    double std_dev;
    double min;
    double max;
    double median;
} DescriptiveStats;

EXPORT_API double calculate_mean(const double* data, int size);
EXPORT_API double calculate_variance(const double* data, int size);
EXPORT_API double calculate_std_dev(const double* data, int size);
EXPORT_API double calculate_percentile(double* data, int size, double p);
EXPORT_API void calculate_descriptive_stats(const double* data, int size, DescriptiveStats* result);
EXPORT_API void calculate_exponential_moving_average(const double* data, int size, double alpha, double* output);
EXPORT_API void calculate_linear_regression(const double* x, const double* y, int size, LinearRegressionResult* result);

#ifdef __cplusplus
}
#endif

#endif // STUDYCHART_STATS_H
