
#ifndef CPP_PROJECT_PATH_H
#define CPP_PROJECT_PATH_H

#include <string>

class Path{

public:
    std::string file_path;
    std::string file_filename;
    std::string full_path;

    Path(){
        file_path = "";
        file_filename = "";
        full_path = file_path + '/' + file_filename;
    }

    Path(std::string file_path_, std::string file_filename_){
        file_path = file_path_;
        file_filename = file_filename_;
        full_path = file_path + '/' + file_filename;
    }
};

#endif //CPP_PROJECT_PATH_H
