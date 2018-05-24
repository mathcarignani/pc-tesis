
#include "string_utils.h"

#include <iostream>
#include <math.h>

//
// SOURCE: https://stackoverflow.com/a/2340309/4547232
//
bool StringUtils::find(std::string string, std::string string_to_find) {
    return (string.find(string_to_find) != std::string::npos);
}

//
// SOURCE: https://stackoverflow.com/a/46943631/4547232
//
std::vector<std::string> StringUtils::splitByString(std::string str, std::string delimiter){
    std::vector<std::string>result;
    int delimiter_size = delimiter.size();
    while(str.size()){
        int index = str.find(delimiter);
        if(index!=std::string::npos){
            result.push_back(str.substr(0,index));
            str = str.substr(index+delimiter_size);
            if(str.size()==0)result.push_back(str);
        }else{
            result.push_back(str);
            str = "";
        }
    }
    return result;
}

//
// SOURCE: https://stackoverflow.com/a/19751779/4547232
//
std::vector<std::string> StringUtils::splitByChar(std::string str, const char delimiter){
    std::vector<std::string> result;
    std::string acc = "";
    for(int i = 0; i < str.size(); i++){
        if(str[i] == delimiter){
            result.push_back(acc);
            acc = "";
        }
        else{
            acc += str[i];
        }
    }
    result.push_back(acc); // here we assume that str[str.size()-1] != delimiter
    return result;
}

std::string StringUtils::splitByCharWithIndex(std::string str, const char delimiter, int index){
    int delimiter_count = 0;
    std::string acc = "";
    for(int i = 0; i < str.size(); i++){
        if (index != delimiter_count){
            if(str[i] == delimiter){
                delimiter_count++;
            }
        }
        else {
            if(str[i] != delimiter){
                acc += str[i];
            }
            else {
                return acc;
            }
        }
    }
}

//
// SOURCE: https://stackoverflow.com/a/36280865/4547232
//
std::string StringUtils::join(std::vector<std::string> arr, std::string token){
    if (arr.empty()) return "";

    std::string str;
    for (auto i : arr)
        str += i + token;
    str = str.substr(0, str.size() - token.size());
    return str;
}


//std::string StringUtils::removeToken(std::string str, std::string token){
////    current_line.erase(std::remove(current_line.begin(), current_line.end(), '\n'), current_line.end());
//    char* new_str = str.erase(std::remove(str.begin(), str.end(), '\n'), str.end());
//    return new_str;
//}

//
// SOURCE: https://stackoverflow.com/a/5891683/4547232
//
std::string StringUtils::removeChars(const std::string& source, const std::string& chars){
    std::string result="";
    for (unsigned int i=0; i<source.length(); i++) {
        bool foundany=false;
        for (unsigned int j=0; j<chars.length() && !foundany; j++) {
            foundany=(source[i]==chars[j]);
        }
        if (!foundany) {
            result+=source[i];
        }
    }
    return result;
}


std::string StringUtils::removeLastChar(const std::string& source){
    std::string result="";
    for (unsigned int i=0; i<source.length() - 1; i++) {
        result+=source[i];
    }
    return result;
}

int StringUtils::charToInt(const char character){
    return (int) character;
}

const char StringUtils::intToChar(const int integer){
    return (char) integer;
}

//
// SOURCE: https://stackoverflow.com/a/21192373/4547232
//
int StringUtils::bitLength(uint32_t value){
    int bits = 0;
    for (int bit_test = 16; bit_test > 0; bit_test >>= 1){
        if (value >> bit_test != 0){
            bits += bit_test;
            value >>= bit_test;
        }
    }
    return bits + value;
}

int StringUtils::doubleToInt(double d){
    int d_int = (int)round(d);
    return d_int;
}

std::string StringUtils::doubleToString(double d){
    int d_int = doubleToInt(d);
    std::string d_string = std::to_string(d_int);
    return d_string;
}
