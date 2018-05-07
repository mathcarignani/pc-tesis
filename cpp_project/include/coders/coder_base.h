
#ifndef CPP_PROJECT_CODER_BASE_H
#define CPP_PROJECT_CODER_BASE_H

#include <string>

class CoderBase {

private:
    void codeDataRowsCount();

    void codeDataRows();

    void codeValue(std::string x, int row_index, int col_index);

    void codeRaw(int value);

    void codeValueRaw(std::string x, int row_index, int col_index);

    void raiseRangeError();


public:
    CoderBase();

    std::string getInfo();

    void codeFile();

    void close();
};

#endif //CPP_PROJECT_CODER_BASE_H
