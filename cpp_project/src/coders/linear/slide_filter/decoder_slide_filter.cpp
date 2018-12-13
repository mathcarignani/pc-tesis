
#include "decoder_slide_filter.h"

#if MASK_MODE

#include "math_utils.h"
#include <cmath>
#include "string_utils.h"
#include "coder_utils.h"

void DecoderSlideFilter::setCoderParams(int window_size_){
    window_size_bit_length = MathUtils::bitLength(window_size_);
}


std::vector<std::string> DecoderSlideFilter::decodeDataColumn(){
    column = new Column(data_rows_count, mask->total_data, mask->total_no_data);
    m_pCompressData = new DynArray<SlideFiltersEntry>();
    decodeEntries();
//    std::cout << "m_pCompressData->size() = " << m_pCompressData->size() << std::endl;

    std::vector<int> x_coords_vector = CoderUtils::createXCoordsVectorMaskMode(mask, time_delta_vector, 1);
    decompress(x_coords_vector);

    std::cout << "m_pApproxData->size() = " << m_pApproxData->size() << std::endl;
    std::cout << "column->unprocessed_data_rows = " << column->unprocessed_data_rows << std::endl;
    std::cout << "data_rows_count = " << data_rows_count << std::endl;

//    assert(m_pApproxData->size() == column->unprocessed_data_rows);

    int pos = 0;
    mask->reset();
    while (column->notFinished()){
        if (mask->isNoData()) {
            column->addNoData();
            continue;
        }
        DataItem data_item = m_pApproxData->getAt(pos);
        std::string value = StringUtils::doubleToString(data_item.value);
        column->addData(value);
//        if (column->unprocessed_rows == 1){
//            std::cout << "VALLL " << value << std::endl;
//        }
        pos++;
    }

    delete m_pCompressData;
    delete m_pApproxData;
    column->assertAfter();
    return column->column_vector;
}

void DecoderSlideFilter::decodeEntries(){
    float size = decodeFloat();
    std::cout << "entries_vector.size() = " << size << std::endl;
    for(int i=0; i < size; i++){
        SlideFiltersEntry* entry = decodeEntry();
        m_pCompressData->add(*entry);

//        std::cout << "codeEntry" << std::endl;
        std::cout << entry->connToFollow << " " << entry->timestamp << " " << entry->value << std::endl;
//        std::cout << "recording.connToFollow " << entry->connToFollow << std::endl;
//        std::cout << "recording.timestamp " << entry->timestamp << std::endl;
//        std::cout << "recording.value " << entry->value << std::endl;
    }
}

SlideFiltersEntry* DecoderSlideFilter::decodeEntry(){
    bool connToFollow = decodeBool();
    float timestamp = decodeFloat();
    float value = decodeFloat();
    SlideFiltersEntry* recording = new SlideFiltersEntry(value, timestamp, connToFollow);
//    std::cout << "decodeEntry" << std::endl;
//    std::cout << "recording.connToFollow " << recording->connToFollow << std::endl;
//    std::cout << "recording.timestamp " << recording->timestamp << std::endl;
//    std::cout << "recording.value " << recording->value << std::endl;
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
void DecoderSlideFilter::decompress(std::vector<int> x_coords_vector)
{
    m_pApproxData = new CDataStream();
    int size = m_pCompressData->size();
    int position = 0;
    double timeStamp = 0;
    int lastTimeStamp = m_pCompressData->getAt(m_pCompressData->size() - 1).timestamp;
    SlideFiltersEntry slEntry1, slEntry2;
    Line* l = NULL;
    DataItem inputEntry;

//    for(int i = 0; i < lastTimeStamp; i++)
    int x_coords_vector_index = 0;
    int i = 0;
    while(i < lastTimeStamp)
    {
        std::cout << "i = " << i << std::endl;
        std::cout << "position = " << position << std::endl;

        //Read compressed data
        if (i >= timeStamp)
        {
            slEntry1 = m_pCompressData->getAt(position);

            if (slEntry1.connToFollow)//Connected
            {
                std::cout << "Connected" << std::endl;
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
                std::cout << "Disconnected" << std::endl;
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
            std::cout << "New line" << std::endl;
            std::cout << "p1=(" << slEntry1.timestamp << ", " << slEntry1.value << ")" << std::endl;
            std::cout << "p2=(" << slEntry2.timestamp << ", " << slEntry2.value << ")" << std::endl;
        }

        i++;
        if (x_coords_vector[x_coords_vector_index] > i) { continue; }

        x_coords_vector_index++;
        //Get point on line at each corresponding time
        inputEntry.timestamp = i;
        inputEntry.value = l->getValue(inputEntry.timestamp);
        m_pApproxData->add(inputEntry);
        std::cout << "add(inputEntry) = (" << inputEntry.timestamp << ", " << inputEntry.value << ")" << std::endl;
    }

    delete l;
}

#endif // MASK_MODE
