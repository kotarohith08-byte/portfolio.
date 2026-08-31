#include "search.h"
#include <stdlib.h>
#include <string.h>

static int min3(int a, int b, int c) {
    int m = a;
    if (b < m) m = b;
    if (c < m) m = c;
    return m;
}

int c_binary_search(const double* arr, int size, double target) {
    if (arr == NULL || size <= 0) return -1;
    int left = 0, right = size - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

int c_interpolation_search(const int* arr, int size, int target) {
    if (arr == NULL || size <= 0) return -1;
    int low = 0, high = size - 1;
    while (low <= high && target >= arr[low] && target <= arr[high]) {
        if (low == high) {
            if (arr[low] == target) return low;
            return -1;
        }
        int pos = low + (((double)(high - low) / (arr[high] - arr[low])) * (target - arr[low]));
        if (pos < low || pos > high) return -1;
        if (arr[pos] == target) return pos;
        if (arr[pos] < target) low = pos + 1;
        else high = pos - 1;
    }
    return -1;
}

int c_levenshtein_distance(const char* s1, const char* s2) {
    if (s1 == NULL || s2 == NULL) return -1;
    int len1 = (int)strlen(s1);
    int len2 = (int)strlen(s2);

    int* d = (int*)malloc((len1 + 1) * (len2 + 1) * sizeof(int));
    if (d == NULL) return -1;

    for (int i = 0; i <= len1; i++) d[i * (len2 + 1) + 0] = i;
    for (int j = 0; j <= len2; j++) d[0 * (len2 + 1) + j] = j;

    for (int i = 1; i <= len1; i++) {
        for (int j = 1; j <= len2; j++) {
            int cost = (s1[i - 1] == s2[j - 1]) ? 0 : 1;
            d[i * (len2 + 1) + j] = min3(
                d[(i - 1) * (len2 + 1) + j] + 1,       // deletion
                d[i * (len2 + 1) + (j - 1)] + 1,       // insertion
                d[(i - 1) * (len2 + 1) + (j - 1)] + cost // substitution
            );
        }
    }

    int result = d[len1 * (len2 + 1) + len2];
    free(d);
    return result;
}
