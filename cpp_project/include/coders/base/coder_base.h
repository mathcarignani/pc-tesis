
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
    virtual void codeCoderParams() = 0;
    virtual void codeDataRows() = 0;
    //
    // This method maps a value read in the csv file into an integer to be written in the output file.
    // It also checks the minimum and maximum constraints.
    //
    int codeValue(std::string x);
    void codeRaw(int value);

protected:
    int window_size;

public:
    CSVReader* input_csv;
    BitStreamWriter* output_file;
    Dataset* dataset;
    int data_rows_count;

    CoderBase(CSVReader* input_csv_, BitStreamWriter* output_file_);
    void codeFile();
    void codeCoderParameters(int coder_code, int window_size);
    void printBits();
    void close();

    void codeBit(int bit);
    void codeBits(int bit, int times);
    void codeBool(bool bit);
    void codeInt(int value, int bits);
    void codeUnary(int value);
    void codeValueRaw(std::string x);
    void codeFloat(float x);
    void codeDouble(double x);
    void codeInt(int x);
    void flushByte();
    void forceFlushByte();
};

#endif //CPP_PROJECT_CODER_BASE_H
