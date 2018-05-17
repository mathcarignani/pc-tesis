
#ifndef CPP_PROJECT_HEADER_UTILS_H
#define CPP_PROJECT_HEADER_UTILS_H

#include <iostream>
#include "datetime_utils.h"


class HeaderUtils {

public:
    static std::string date_format() { return "%Y-%m-%d %H:%M:%S"; }; // "2010-10-01 00:00:00"
    static std::tm start_date() { return DatetimeUtils::parseDate("1900-01-01 00:00:00", date_format()); };
    static std::tm end_date() { return DatetimeUtils::parseDate("2036-02-07 06:28:16", date_format()); };

};

#endif //CPP_PROJECT_HEADER_UTILS_H
