
#ifndef CPP_PROJECT_CODER_BASE_H
#define CPP_PROJECT_CODER_BASE_H

#include <string>
#include "bit_stream_writer.h"
#include "csv_reader.h"
#include "dataset.h"
#include "constants.h"


class CoderBase {

private:
    void codeDataRowsCount();
    virtual void codeDataRows() = 0;
    //
    // This method maps a value read in the csv file into an integer to be written in the output file.
    // It also checks the minimum and maximum constraints.
    //
    int codeValue(std::string x);
    void codeRaw(int value);
//    virtual void raiseRangeError(int value) = 0;

protected:
    CSVReader &input_csv;
    BitStreamWriter &output_file;
    Dataset dataset;

    void codeBit(int bit);
    void codeValueRaw(std::string x);
    void codeFloat(float x);

public:
    CoderBase(CSVReader &input_csv, BitStreamWriter &output_file) : input_csv(input_csv), output_file(output_file) { }
    void codeFile();
    void printBits();
    void close();
};

#endif //CPP_PROJECT_CODER_BASE_H
