
#include "string_utils.h"
#include <iostream>
#include <string>

//
// SOURCE: https://stackoverflow.com/a/46943631/4547232
//
std::vector<std::string> StringUtils::split(std::string str, std::string token){
    std::vector<std::string>result;
    while(str.size()){
        int index = str.find(token);
        if(index!=std::string::npos){
            result.push_back(str.substr(0,index));
            str = str.substr(index+token.size());
            if(str.size()==0)result.push_back(str);
        }else{
            result.push_back(str);
            str = "";
        }
    }
    return result;
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
std::string StringUtils::RemoveChars(const std::string& source, const std::string& chars){
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
