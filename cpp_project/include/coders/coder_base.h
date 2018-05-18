
#ifndef CPP_PROJECT_CODER_BASE_H
#define CPP_PROJECT_CODER_BASE_H

#include <string>
#include "bit_stream_writer.h"
#include "csv_reader.h"
#include "dataset.h"


class CoderBase {

private:
    void codeDataRowsCount();
    virtual void codeDataRows() = 0;
    //
    // This method maps a value read in the csv file into an integer to be written in the output file.
    // It also checks the minimum and maximum constraints.
    //
    int codeValue(std::string x, int row_index, int col_index);
    void codeRaw(int value);
    void raiseRangeError();

protected:
    CSVReader &input_csv;
    BitStreamWriter &output_file;
    Dataset dataset;
    int columns_count = 0; // number of columns in the csv file

    void codeValueRaw(std::string x, int row_index, int col_index);

public:
    CoderBase(CSVReader &input_csv, BitStreamWriter &output_file) : input_csv(input_csv), output_file(output_file) { }
//    virtual std::string getInfo() = 0;
    void codeFile();
    void close();
};

#endif //CPP_PROJECT_CODER_BASE_H