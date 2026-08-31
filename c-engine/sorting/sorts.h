#ifndef STUDYCHART_SORTS_H
#define STUDYCHART_SORTS_H

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _WIN32
  #define EXPORT_API __declspec(dllexport)
#else
  #define EXPORT_API __attribute__((visibility("default")))
#endif

EXPORT_API void c_quicksort(double* arr, int low, int high);
EXPORT_API void c_mergesort(double* arr, int l, int r);
EXPORT_API void c_radixsort(int* arr, int n);

#ifdef __cplusplus
}
#endif

#endif // STUDYCHART_SORTS_H
