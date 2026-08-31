#include "sorts.h"
#include <stdlib.h>

static void swap(double* a, double* b) {
    double temp = *a;
    *a = *b;
    *b = temp;
}

static int partition(double* arr, int low, int high) {
    double pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void c_quicksort(double* arr, int low, int high) {
    if (arr == NULL || low >= high) return;
    int pi = partition(arr, low, high);
    c_quicksort(arr, low, pi - 1);
    c_quicksort(arr, pi + 1, high);
}

static void merge(double* arr, int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;

    double* L = (double*)malloc(n1 * sizeof(double));
    double* R = (double*)malloc(n2 * sizeof(double));
    if (L == NULL || R == NULL) {
        if (L) free(L);
        if (R) free(R);
        return;
    }

    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];

    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }

    free(L);
    free(R);
}

void c_mergesort(double* arr, int l, int r) {
    if (arr == NULL || l >= r) return;
    int m = l + (r - l) / 2;
    c_mergesort(arr, l, m);
    c_mergesort(arr, m + 1, r);
    merge(arr, l, m, r);
}

static int getMax(int* arr, int n) {
    int mx = arr[0];
    for (int i = 1; i < n; i++)
        if (arr[i] > mx) mx = arr[i];
    return mx;
}

static void countSort(int* arr, int n, int exp) {
    int* output = (int*)malloc(n * sizeof(int));
    if (output == NULL) return;
    int count[10] = {0};

    for (int i = 0; i < n; i++)
        count[(arr[i] / exp) % 10]++;

    for (int i = 1; i < 10; i++)
        count[i] += count[i - 1];

    for (int i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }

    for (int i = 0; i < n; i++)
        arr[i] = output[i];

    free(output);
}

void c_radixsort(int* arr, int n) {
    if (arr == NULL || n <= 1) return;
    int m = getMax(arr, n);
    for (int exp = 1; m / exp > 0; exp *= 10)
        countSort(arr, n, exp);
}
