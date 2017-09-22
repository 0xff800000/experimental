/*
g++ -Wall -fPIC -c x10.cpp 
g++ -shared -o libshared.so x10.o -ldl -lstdc++
LD_PRELOAD=$PWD/libshared.so app
*/

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <dlfcn.h>
#include <stdio.h>

static timeval * timezero = 0;

typedef int (*go)(timeval *tv, timezone *tz);

extern "C" int gettimeofday(timeval *tv, timezone *tz)
{
    // Testing purposes:
    go gettimeofday_orig;
    int val;
    gettimeofday_orig=(go)dlsym(RTLD_NEXT,"gettimeofday");
    if (!timezero)
    {
        timezero = new timeval;
        val = gettimeofday_orig(timezero,tz);
        (*tv) = (*timezero);
        return val;
    }
    // Multiply speed:
    int M = 200;
    // Divide speed:
    int N = 10;
    // That means 1/2 speed;

    val = gettimeofday_orig(tv,tz);
    // Multiply the seconds:
    tv->tv_sec = M*tv->tv_sec - M*timezero->tv_sec + N*timezero->tv_sec;
    // Multiply the microseconds:
    tv->tv_usec = M*tv->tv_usec - M*timezero->tv_usec + N*timezero->tv_usec;
    // Add the modulus of seconds to microseconds:
    tv->tv_usec += ((tv->tv_sec % N) * 1000000);
    tv->tv_sec /= N;
    tv->tv_usec /= N;
    while(tv->tv_usec >= 1000000)
    {
        tv->tv_usec -= 1000000;
        tv->tv_sec += 1;
    }
    while(tv->tv_usec < 0)
    {
        tv->tv_usec += 1000000;
        tv->tv_sec -= 1;
    }
    return val;
}