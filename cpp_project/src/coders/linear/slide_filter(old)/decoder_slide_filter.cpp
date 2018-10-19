
#include "decoder_slide_filter.h"

#if MASK_MODE

#include "decoder_base.h"
#include "math_utils.h"
#include <cmath>
#include "string_utils.h"

void DecoderSlideFilter::setCoderParams(int window_size_){
    window_size_bit_length = MathUtils::bitLength(window_size_);
}


std::vector<std::string> DecoderSlideFilter::decodeDataColumn(){
    column = new Column(data_rows_count, total_data, total_no_data);

    std::vector<DataItem> data_item_array = decompress();
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

SlideFiltersEntry* DecoderSlideFilter::decodeEntry(){
    bool connToFollow = decodeBool();
    float timestamp = decodeFloat();
    float value = decodeFloat();
    SlideFiltersEntry* recording = new SlideFiltersEntry(value, timestamp, connToFollow);
    std::cout << "decodeEntry" << std::endl;
    std::cout << "recording.connToFollow " << recording->connToFollow << std::endl;
    std::cout << "recording.timestamp " << recording->timestamp << std::endl;
    std::cout << "recording.value " << recording->value << std::endl;
    return recording;
}

SlideFiltersEntry* DecoderSlideFilter::getAt(std::vector<SlideFiltersEntry*> & m_pCompressData, int position){
    std::cout << "position = " << position << std::endl;
    int diff = position + 1 - m_pCompressData.size();

    while(diff > 0){
        SlideFiltersEntry* entry = decodeEntry();
        m_pCompressData.push_back(entry);
        diff--;
    }
    return m_pCompressData.at(position);
}

// Calculate approximation data from model parameters
//void SlideFiltersOutput::decompressData()
std::vector<DataItem> DecoderSlideFilter::decompress()
{
    std::vector<int> x_coord = CoderUtils::createXCoordsVector(mask, time_delta_vector, total_data);
    std::vector<SlideFiltersEntry*> m_pCompressData;

    std::vector<DataItem> m_pApproxData; // m_pApproxData = new CDataStream();
    // int size = m_pCompressData->size();
    int position = 0;
    double timeStamp = 0;
    int lastTimeStamp = x_coord[total_data]; // m_pCompressData->getAt(m_pCompressData->size() - 1).timestamp;
    SlideFiltersEntry *slEntry1, *slEntry2;
    Line* l = NULL;
    DataItem inputEntry;

//    for(int i = 0; i < lastTimeStamp; i++)
    int i = 0;
    for(int i_index = 0; i_index < total_data; i_index++)
    {
        i = x_coord[i_index];

        //Read compressed data
        if (i >= timeStamp)
        {
            slEntry1 = getAt(m_pCompressData, position); // m_pCompressData->getAt(position);

            if (slEntry1->connToFollow)//Connected
            {
                position++;
                slEntry2 = getAt(m_pCompressData, position); // m_pCompressData->getAt(position);

                //Go back for second reading
                if (slEntry2->connToFollow)
                {
                    timeStamp = slEntry2->timestamp - 1;
                }
                else
                {
                    position++;
                    timeStamp = slEntry2->timestamp;
                }
            }
            else //Disconnected
            {
                inputEntry.timestamp = slEntry1->timestamp;
                inputEntry.value = slEntry1->value;
                m_pApproxData.push_back(inputEntry); // m_pApproxData->add(inputEntry);
                break;
            }

            //Create line go through two point in compressed data
            if (l != NULL)
            {
                delete l;
            }

            Point p1(slEntry1->value, slEntry1->timestamp);
            Point p2(slEntry2->value, slEntry2->timestamp);
            l = new Line(&p1, &p2);
        }

        //Get point on line at each corresponding time
        inputEntry.timestamp = x_coord[i_index + 1]; // i + 1;
        inputEntry.value = l->getValue(inputEntry.timestamp);
        m_pApproxData.push_back(inputEntry); // m_pApproxData->add(inputEntry);
    }

    delete l;
    return m_pApproxData;
}

#endif // MASK_MODE
