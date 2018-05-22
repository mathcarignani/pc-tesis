#ifndef _REDEF_
#define _REDEF_

#include "iniparser/iniparser.h"
#include <ctype.h>
#include <limits.h>
//#include <sys/types.h>
#include <time.h>
#include <sys/time.h>


#define MAX_PATH PATH_MAX
#define __int64 int64_t

typedef unsigned long DWORD;
typedef int64_t LONGLONG;
typedef union _LARGE_INTEGER {
    struct {
        DWORD LowPart;
        DWORD HighPart;
    };
    LONGLONG QuadPart;
} LARGE_INTEGER, *PLARGE_INTEGER;

/*#define INVALID_HANDLE_VALUE NULL
#define FALSE 0

typedef int64_t __int64;
typedef void* HANDLE;
typedef void* LPVOID;


typedef int BOOL;

typedef struct _FILETIME {
    DWORD dwLowDateTime;
    DWORD dwHighDateTime;
} FILETIME, *PFILETIME;



typedef struct _WIN32_FIND_DATAA {
    DWORD dwFileAttributes;
    FILETIME ftCreationTime;
    FILETIME ftLastAccessTime;
    FILETIME ftLastWriteTime;
    DWORD nFileSizeHigh;
    DWORD nFileSizeLow;
    DWORD dwReserved0;
    DWORD dwReserved1;
    char cFileName[MAX_PATH];
    char cAlternateFileName[14];
} WIN32_FIND_DATAA;


// This part is dedicated to the manual implementation of strup() as conio.h should be removed to run in Linux
// Portable, public domain replacements for strupr() & strlwr() by Bob Stout
//

void FindClose(HANDLE handle) {
    free(handle);
}
*/
void QueryPerformanceCounter(LARGE_INTEGER* f);
void QueryPerformanceFrequency(LARGE_INTEGER* f);
char *strupr(char *string);
char *strlwr(char *string);
char* itoa(int value, char* result, int base);
#endif
