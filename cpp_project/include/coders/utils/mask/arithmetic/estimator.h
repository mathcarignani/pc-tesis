
#ifndef CPP_PROJECT_ESTIMATOR_H
#define CPP_PROJECT_ESTIMATOR_H

class Estimator {

private:
    static const double DIV;

    // counters for when the last value read is data
    int m_data; // data count
    int n_data; // nodata count
    int total_data; // m_data + n_data

    // counters for when the last value read is nodata
    int m_nodata; // data count
    int n_nodata; // nodata count
    int total_nodata; // m_nodata + n_nodata

    bool nodata; // current state (true if the last value read is nodata)

public:
    Estimator();
    double estimateProbability(bool no_data_);
    double estimateEOFProbability();
    void print();
};

#endif //CPP_PROJECT_ESTIMATOR_H
