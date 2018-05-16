
#include "datetime_utils.h"

#include <iomanip>
#include <sstream>
#include "assert.h"
#include <vector>

std::tm DatetimeUtils::parseDate(std::string tm_str, std::string datetime_format){
    std::tm tm;
    std::memset(&tm, 0, sizeof(std::tm));
    std::istringstream ss(tm_str);
    ss >> std::get_time(&tm, datetime_format.c_str());
    return tm;
}

int DatetimeUtils::compareDates(std::tm date1, std::tm date2) {
    if(date1.tm_year < date2.tm_year){ return 1; }
    else if(date2.tm_year < date1.tm_year){ return -1; }

    if(date1.tm_yday < date2.tm_yday){ return 1; }
    else if(date2.tm_yday < date1.tm_yday){ return -1; }

    if(date1.tm_hour < date2.tm_hour){ return 1; }
    else if(date2.tm_hour < date1.tm_hour){ return -1; }

    if(date1.tm_min < date2.tm_min){ return 1; }
    else if(date2.tm_min < date1.tm_min){ return -1; }

    if(date1.tm_sec < date2.tm_sec){ return 1; }
    else if(date2.tm_sec < date1.tm_sec){ return -1; }

    return 0;
}

long int DatetimeUtils::datetimeToSecondsSince(std::tm start_date, std::tm date){
    assert(compareDates(start_date, date) != -1);
    assert(start_date.tm_year == 0 and start_date.tm_mon == 0 and start_date.tm_mday == 1);
    assert(start_date.tm_hour == 0 and start_date.tm_min == 0 and start_date.tm_sec == 0);

    long int seconds = 0;
    for(int i=0; i < date.tm_year; i++){ seconds += secondsInYear(1900 + i); }
    for(int i=0; i < daysSinceJanuary1(date); i++){ seconds += secondsInDay(); }
    for(int i=0; i < date.tm_hour; i++){ seconds += secondsInHour(); }
    for(int i=0; i < date.tm_min; i++){ seconds += secondsInMinute(); }
    seconds += date.tm_sec;

    return seconds;
}

int DatetimeUtils::secondsInYear(int year){
    int day_count = 365;
    if (isLeapYear(year)){ day_count++; }
    return day_count*secondsInDay();
}

int DatetimeUtils::daysSinceJanuary1(std::tm date){
    std::vector<int> days_per_month = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int day_count = 0;
    for(int i=0; i < date.tm_mon; i++){
        day_count += days_per_month[i];
        if (i==1 and isLeapYear(date.tm_year)) { day_count++; }
    }
    day_count += date.tm_mday - 1;
    return day_count;
}

int DatetimeUtils::secondsInDay(){
    return 24*secondsInHour();
}

int DatetimeUtils::secondsInHour(){
    return 60*secondsInMinute();
}

int DatetimeUtils::secondsInMinute(){
    return 60;
}

bool DatetimeUtils::isLeapYear(int year){
    if (year % 4 == 0){
        if (year % 100 == 0)
        {
            return (year % 400 == 0);
        }
        else
            return true;
    }
    else {
        return false;
    }
}
