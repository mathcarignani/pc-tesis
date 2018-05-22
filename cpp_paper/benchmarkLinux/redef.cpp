#include "redef.h"
void QueryPerformanceCounter(LARGE_INTEGER* f) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    f->QuadPart =  tv.tv_usec * 1000;
    // actually, tv.tv_usec only reaches microsecond, thus multiplied it by 1000 just converts to a very approximate number of nanoseconds
}

void QueryPerformanceFrequency(LARGE_INTEGER* f) {
    f->QuadPart = CLOCKS_PER_SEC;
}

char *strupr(char *string) {
    char *s;
    if (string) {
        for (s = string; *s; ++s)
            *s = toupper(*s);
    }
    return string;
}

char *strlwr(char *string) {
    char *s;
    if (string) {
        for (s = string; *s; ++s)
            *s = tolower(*s);
    }
    return string;
}

char* itoa(int value, char* result, int base) {
    // check that the base if valid
    if (base < 2 || base > 36) { *result = '\0'; return result; }
    char* ptr = result, *ptr1 = result, tmp_char;
    int tmp_value;
    do {
        tmp_value = value;
        value /= base;
        *ptr++ = "zyxwvutsrqponmlkjihgfedcba9876543210123456789abcdefghijklmnopqrstuvwxyz" [35 + (tmp_value - value * base)];
    } while ( value );
    // Apply negative sign
    if (tmp_value < 0) *ptr++ = '-';
    *ptr-- = '\0';
    while(ptr1 < ptr) {
        tmp_char = *ptr;
        *ptr--= *ptr1;
        *ptr1++ = tmp_char;
    }
    return result;
}
