
#ifndef MODEL_KT_DOT_H
#define MODEL_KT_DOT_H

#define SYMBOL_COUNT 3 // original: 257
#define ARRAY_SIZE 4 // original: 258
#define EOF_CODE 2 // original: 256

#include <iostream>
#include <stdexcept>
#include "model_metrics.h"

template<typename CODE_VALUE_ = unsigned int,
        int CODE_VALUE_BITS_ = (std::numeric_limits<CODE_VALUE_>::digits + 3) / 2,
        int FREQUENCY_BITS_ = std::numeric_limits<CODE_VALUE_>::digits - CODE_VALUE_BITS_>
struct modelKT : public model_metrics<CODE_VALUE_, CODE_VALUE_BITS_, FREQUENCY_BITS_>
{
    typedef model_metrics<CODE_VALUE_, CODE_VALUE_BITS_, FREQUENCY_BITS_> metrics;
    typedef typename metrics::prob prob;
    typedef CODE_VALUE_ CODE_VALUE;
    using metrics::MAX_CODE;
    using metrics::MAX_FREQ;
    using metrics::CODE_VALUE_BITS;
    using metrics::ONE_FOURTH;
    using metrics::ONE_HALF;
    using metrics::THREE_FOURTHS;
    //
    // variables used by the model
    //
    CODE_VALUE cumulative_frequency[ARRAY_SIZE];
    //Character a is defined by the range cumulative_frequency[a],
    //cumulative_frequency[a+1], with cumulative_frequency[257]
    //containing the total count for the model. Note that entry
    //256 is the EOF.
    unsigned long long m_bytesProcessed;
    static_assert( MAX_FREQ > SYMBOL_COUNT, "Not enough code bits to represent the needed symbol library" );

    modelKT()
    {
        reset();
    }
    void reset()
    {
        for ( int i = 0 ; i < ARRAY_SIZE ; i++ )
            cumulative_frequency[i] = i;
        m_bytesProcessed = 0;
        m_frozen = false;
    }
    virtual inline void pacify()
    {
        if ( (++m_bytesProcessed % 1000) == 0 )
            std::cout << m_bytesProcessed << "\r";
    }
    virtual void frozen()
    {
        std::cout << "Frozen at: " << m_bytesProcessed << "\n";
    }
    void inline update(int c)
    {
        for ( int i = c + 1 ; i < ARRAY_SIZE ; i++ )
            cumulative_frequency[i]++;
        if ( cumulative_frequency[SYMBOL_COUNT] >= MAX_FREQ ) {
            m_frozen = true;
            frozen();
        }
    }
    prob getProbability(int c)
    {
        prob p = { cumulative_frequency[c], cumulative_frequency[c+1], cumulative_frequency[SYMBOL_COUNT] };
        if ( !m_frozen )
            update(c);
        pacify();
        return p;
    }
    prob getChar(CODE_VALUE scaled_value, int &c)
    {
        pacify();
        for ( int i = 0 ; i < SYMBOL_COUNT ; i++ )
            if ( scaled_value < cumulative_frequency[i+1] ) {
                c = i;
                prob p = {cumulative_frequency[i], cumulative_frequency[i+1],cumulative_frequency[SYMBOL_COUNT]};
                if ( !m_frozen)
                    update(c);
                return p;
            }
        throw std::logic_error("error");
    }
    CODE_VALUE getCount()
    {
        return cumulative_frequency[SYMBOL_COUNT];
    }
    bool m_frozen;

};

#endif //#ifndef MODEL_KT_DOT_H
