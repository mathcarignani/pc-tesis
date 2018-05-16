
#ifndef CPP_PROJECT_DATETIME_UTILS_H
#define CPP_PROJECT_DATETIME_UTILS_H

#include <iostream>


class DatetimeUtils {

public:
    static std::tm parseDate(std::string tm_str, std::string datetime_format);
    static int compareDates(std::tm date1, std::tm date2);
    static long int datetimeToSecondsSince(std::tm start_date, std::tm date);

private:
    static int secondsInYear(int year);
    static int daysSinceJanuary1(std::tm date);
    static int secondsInDay();
//    static int secondsInMonth(int year, int month);
    static int secondsInHour();
    static int secondsInMinute();
    static bool isLeapYear(int year);
};

#endif //CPP_PROJECT_DATETIME_UTILS_H
