
#include "decoder_slide_filter.h"
#include "decoder_base.h"
#include "math_utils.h"
#include <cmath>
#include "constants.h"
#include "string_utils.h"

void DecoderSlideFilter::setCoderParams(int max_window_size_){
    max_window_size_bit_length = MathUtils::bitLength(max_window_size_);
}


std::vector<std::string> DecoderSlideFilter::decodeDataColumn(){
    column = new Column(data_rows_count, total_data, total_no_data);

    std::vector<DataItem> data_item_array = decompressData();
    assert(data_item_array.size() == total_data);

    int pos = 0;
    mask->reset();
    while (column->unprocessed_rows > 0){
        if (mask->isNoData()) {
            column->addNoData();
            continue;
        }
        DataItem data_item = data_item_array.at(pos);
        std::string value = StringUtils::doubleToString(data_item.value);
        column->addData(value);
        pos++;
    }

    column->assertAfter();
    return column->column_vector;
}

SlideFiltersEntry DecoderSlideFilter::decodeEntry(){
    bool connToFollow = decodeBool();
    float timestamp = decodeFloat();
    float value = decodeFloat();
    SlideFiltersEntry recording(value, timestamp, connToFollow);
    std::cout << "decodeEntry" << std::endl;
    std::cout << "recording.connToFollow " << recording.connToFollow << std::endl;
    std::cout << "recording.timestamp " << recording.timestamp << std::endl;
    std::cout << "recording.value " << recording.value << std::endl;
    return recording;
}

// Calculate approximation data from model parameters
void SlideFiltersOutput::decompressData()
{
    m_pApproxData = new CDataStream();
    int size = m_pCompressData->size();
    int position = 0;
    double timeStamp = 0;
    int lastTimeStamp = m_pCompressData->getAt(m_pCompressData->size() - 1).timestamp;
    SlideFiltersEntry slEntry1, slEntry2;
    Line* l = NULL;
    DataItem inputEntry;

    for(int i = 0; i < lastTimeStamp; i++)
    {
        //Read compressed data
        if (i >= timeStamp)
        {
            slEntry1 = m_pCompressData->getAt(position);

            if (slEntry1.connToFollow)//Connected
            {
                position++;
                slEntry2 = m_pCompressData->getAt(position);

                //Go back for second reading
                if (slEntry2.connToFollow)
                {
                    timeStamp = slEntry2.timestamp - 1;
                }
                else
                {
                    position++;
                    timeStamp = slEntry2.timestamp;
                }
            }
            else //Disconnected
            {
                inputEntry.timestamp = slEntry1.timestamp;
                inputEntry.value = slEntry1.value;
                m_pApproxData->add(inputEntry);
                break;
            }

            //Create line go through two point in compressed data
            if (l != NULL)
            {
                delete l;
            }

            Point p1(slEntry1.value, slEntry1.timestamp);
            Point p2(slEntry2.value, slEntry2.timestamp);
            l = new Line(&p1, &p2);
        }

        //Get point on line at each corresponding time
        inputEntry.timestamp = i + 1;
        inputEntry.value = l->getValue(inputEntry.timestamp);
        m_pApproxData->add(inputEntry);
    }

    delete l;
}