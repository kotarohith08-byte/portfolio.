#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../statistics/stats.h"
#include "../sorting/sorts.h"
#include "../searching/search.h"

int main() {
    printf("========================================\n");
    printf("StudyChart AI - C Algorithm Engine Benchmark\n");
    printf("========================================\n");

    const int N = 100000;
    double* data = (double*)malloc(N * sizeof(double));
    if (!data) {
        printf("Memory allocation error\n");
        return 1;
    }

    srand((unsigned int)time(NULL));
    for (int i = 0; i < N; ++i) {
        data[i] = (double)(rand() % 10000) / 10.0;
    }

    clock_t start = clock();
    DescriptiveStats stats;
    calculate_descriptive_stats(data, N, &stats);
    clock_t end = clock();
    double time_stats = ((double)(end - start)) / CLOCKS_PER_SEC * 1000.0;

    printf("Descriptive Stats (N=%d):\n", N);
    printf("  Mean: %.2f, StdDev: %.2f, Min: %.2f, Max: %.2f, Median: %.2f\n",
           stats.mean, stats.std_dev, stats.min, stats.max, stats.median);
    printf("  Execution Time: %.2f ms\n\n", time_stats);

    start = clock();
    c_quicksort(data, 0, N - 1);
    end = clock();
    double time_sort = ((double)(end - start)) / CLOCKS_PER_SEC * 1000.0;

    printf("QuickSort (N=%d):\n", N);
    printf("  Sorted Check: [%.1f, %.1f, ..., %.1f]\n", data[0], data[1], data[N - 1]);
    printf("  Execution Time: %.2f ms\n\n", time_sort);

    double target = data[N / 2];
    start = clock();
    int idx = c_binary_search(data, N, target);
    end = clock();
    double time_search = ((double)(end - start)) / CLOCKS_PER_SEC * 1000.0;

    printf("Binary Search Target (%.1f):\n", target);
    printf("  Found at Index: %d\n", idx);
    printf("  Execution Time: %.4f ms\n", time_search);

    free(data);
    printf("========================================\n");
    return 0;
}
