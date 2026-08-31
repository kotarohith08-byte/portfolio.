#ifndef STUDYCHART_SEARCH_H
#define STUDYCHART_SEARCH_H

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _WIN32
  #define EXPORT_API __declspec(dllexport)
#else
  #define EXPORT_API __attribute__((visibility("default")))
#endif

EXPORT_API int c_binary_search(const double* arr, int size, double target);
EXPORT_API int c_interpolation_search(const int* arr, int size, int target);
EXPORT_API int c_levenshtein_distance(const char* s1, const char* s2);

#ifdef __cplusplus
}
#endif

#endif // STUDYCHART_SEARCH_H
