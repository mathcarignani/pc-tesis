
#include "estimator.h"
#include <iostream>

Estimator::Estimator(){
    m_data = 0, n_data = 0;
    total_data = m_data + n_data;

    m_nodata = 0, n_nodata = 0;
    total_nodata = m_nodata + n_nodata;

    nodata = false;
}

double Estimator::estimateProbability(bool no_data_){
    double dividend;
    int new_total;
    if (nodata){ // last value read is nodata
        new_total = ++total_nodata;
        dividend = (no_data_? n_nodata++ : m_nodata++) + 0.5;
    }
    else { // last value read is data
        new_total = ++total_data;
        dividend = (no_data_? n_data++ : m_data++) + 0.5;
    }
    double res = dividend / new_total;
    nodata = no_data_;
    return res;
}

void Estimator::print(){
    if (nodata){
        std::cout << "total_nodata = " << total_nodata << ", m_nodata = " << m_nodata << ", n_nodata = " << n_nodata << std::endl;
    }
    else {
        std::cout << "total_data = " << total_data << ", m_data = " << m_data << ", n_data = " << n_data << std::endl;
    }
    std::cout << std::endl;
}
