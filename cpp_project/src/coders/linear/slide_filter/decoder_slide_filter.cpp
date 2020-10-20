
#include "decoder_slide_filter.h"

#if MASK_MODE

#include "vector_utils.h"
#include "math_utils.h"
#include <cmath>
#include "conversor.h"
#include "coder_utils.h"
#include "line_utils.h"

std::vector<std::string> DecoderSlideFilter::decodeDataColumn(){
    column = new Column(data_rows_count, mask->total_data, mask->total_no_data);

    if (mask->total_data > 0){
        m_pCompressData = new DynArray<SlideFiltersEntry>();
//        std::cout << "decodeEntries" << std::endl;
        decodeEntries();

//        std::cout << "CoderUtils::createXCoordsVectorMaskMode" << std::endl;
//        VectorUtils::printIntVector(time_delta_vector);
        std::vector<int> x_coords_vector = CoderUtils::createXCoordsVectorMaskModeSF(mask, time_delta_vector, 1);
//        VectorUtils::printIntVector(x_coords_vector);

//        std::cout << "decompress" << std::endl;
        decompress(x_coords_vector);
//        std::cout << "m_pApproxData->size() = " << m_pApproxData->size() << std::endl;
//        std::cout << "column->unprocessed_data_rows = " << column->unprocessed_data_rows << std::endl;
//        std::cout << "data_rows_count = " << data_rows_count << std::endl;
        assert(m_pApproxData->size() == column->unprocessed_data_rows);
    }

    int pos = 0;
    mask->reset();
    while (column->notFinished()){
        if (mask->isNoData()) {
            column->addNoData();
            continue;
        }
        DataItem data_item = m_pApproxData->getAt(pos);
        std::string value = Conversor::doubleToIntToString(data_item.value);
        column->addData(value);
        pos++;
    }

    if (mask->total_data > 0){
        delete m_pCompressData;
        delete m_pApproxData;
    }
    column->assertAfter();
    return column->column_vector;
}


int DecoderSlideFilter::calculateLastDataTimestamp(){
    bool data_read = false;
    int first_data_timestamp = 0;
    int last_timestamp = 0;
    int last_data_timestamp = 0;
    int td_size = (int) time_delta_vector.size();
    mask->reset();
    for (int i=0; i < td_size; i++){
        last_timestamp += time_delta_vector.at(i);
        if (!mask->isNoData()) {
            last_data_timestamp = last_timestamp;
            if (!data_read){
                first_data_timestamp = last_timestamp;
                data_read = true;

            }
        }
    }
//    std::cout << "first_data_timestamp = " << first_data_timestamp << std::endl;
//    std::cout << "last_timestamp = " << last_timestamp << std::endl;
//    std::cout << "last_data_timestamp = " << last_data_timestamp << std::endl;
    return last_data_timestamp - first_data_timestamp;
}

void DecoderSlideFilter::decodeEntries(){
    int last_data_timestamp = calculateLastDataTimestamp();
    int current_td = 0;
    while(current_td <= last_data_timestamp){
        SlideFiltersEntry* entry = decodeEntry();
        m_pCompressData->add(*entry);
//        std::cout << "decodeEntry" << std::endl;
//        std::cout << entry->connToFollow << " " << entry->timestamp << " " << entry->value << std::endl;
        current_td = (int) entry->timestamp;
    }

//    float size = decodeFloat();
////    std::cout << "entries_vector.size() = " << size << std::endl;
//    for(int i=0; i < size; i++){
//        SlideFiltersEntry* entry = decodeEntry();
//        m_pCompressData->add(*entry);
////        std::cout << "decodeEntry" << std::endl;
////        std::cout << entry->connToFollow << " " << entry->timestamp << " " << entry->value << std::endl;
//    }
}

SlideFiltersEntry* DecoderSlideFilter::decodeEntry(){
    bool connToFollow = decodeBool();
    double timestamp = decodeDouble();
    double value = decodeDouble();
    SlideFiltersEntry* recording = new SlideFiltersEntry(value, timestamp, connToFollow);
    std::cout << "decodeEntry" << std::endl;
    std::cout << "recording.connToFollow " << recording->connToFollow << std::endl;
    std::cout << "recording.timestamp " << recording->timestamp << std::endl;
    std::cout << "recording.value " << recording->value << std::endl;
    return recording;
}

SlideFiltersEntry* DecoderSlideFilter::getAt(std::vector<SlideFiltersEntry*> & m_pCompressData, int position){
//    std::cout << "position = " << position << std::endl;
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
    SlideFiltersEntry slEntry1, slEntry2;
    DataItem inputEntry;

    if (size == 1){
        slEntry1 = m_pCompressData->getAt(0);
        inputEntry.timestamp = slEntry1.timestamp;
        inputEntry.value = slEntry1.value;
        m_pApproxData->add(inputEntry);
        return;
    }

    int position = 0;
    double timeStamp = 0;
    int first_coord = x_coords_vector.at(0);
    int lastTimeStamp = m_pCompressData->getAt(m_pCompressData->size() - 1).timestamp;
    Line* l = NULL;

//    for(int i = 0; i < lastTimeStamp; i++)
    int x_coords_vector_index = 0;
    int i = 0;
    while(i < lastTimeStamp)
    {
        //Read compressed data
        if (i >= timeStamp)
        {
//            std::cout << "i >= timeStamp" << std::endl;
//            std::cout << "VAL_POSITION = " << position << std::endl;
//            std::cout << "VAL_I = " << i << std::endl;
//            std::cout << "VAL_TIMESTAMP = " << timeStamp << std::endl;
//            std::cout << "----------------------------------------------------------" << std::endl;

            slEntry1 = m_pCompressData->getAt(position);

            if (slEntry1.connToFollow)//Connected
            {
//                std::cout << "Connected" << std::endl;
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
//                std::cout << "    Disconnected" << std::endl;
                inputEntry.timestamp = slEntry1.timestamp;
                inputEntry.value = slEntry1.value;
                m_pApproxData->add(inputEntry);
//                std::cout << "    add(inputEntry) = (" << inputEntry.timestamp << ", " << inputEntry.value << ") ********************************************************" << std::endl;
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
//            std::cout << "    New line" << std::endl;
//            std::cout << "    p1=(" << slEntry1.timestamp << ", " << slEntry1.value << ")" << std::endl;
//            std::cout << "    p2=(" << slEntry2.timestamp << ", " << slEntry2.value << ")" << std::endl;
        }

        i++;
        if (x_coords_vector[x_coords_vector_index] >= i + first_coord) { continue; }

//        std::cout << "VAL_POSITION = " << position << std::endl;
//        std::cout << "VAL_I = " << i << std::endl;
//        std::cout << "VAL_TIMESTAMP = " << timeStamp << std::endl;
//        std::cout << "----------------------------------------------------------" << std::endl;

        x_coords_vector_index++;
        //Get point on line at each corresponding time
        inputEntry.timestamp = i;
        inputEntry.value = l->getValue(inputEntry.timestamp);
        m_pApproxData->add(inputEntry);
//        std::cout << "    add(inputEntry) = (" << inputEntry.timestamp << ", " << inputEntry.value << ") ********************************************************" << std::endl;
    }

    delete l;
}

#endif // MASK_MODE
