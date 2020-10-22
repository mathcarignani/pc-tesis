
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
        std::vector<int> x_coords_vector = CoderUtils::createXCoordsVectorMaskModeSF(mask, time_delta_vector, 1);
        int lastTimeStamp = calculateLastDataTimestamp() + 1;
//    std::cout << "lastTimeStamp = " << lastTimeStamp << std::endl;
        decompress(x_coords_vector, lastTimeStamp);
        assert(column->unprocessed_data_rows == 0);
    }
    while (column->notFinished()) {
        column->addNoData();
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
    int zero_sum = -1; // -1 instead of 0, to avoid counting the first entry, which is always 0
    mask->reset();
    for (int i=0; i < td_size; i++){
        int timestamp = time_delta_vector.at(i);
        if (timestamp == 0){ zero_sum += 1; }
        last_timestamp += timestamp;
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
    last_data_timestamp += zero_sum;
    return last_data_timestamp - first_data_timestamp;
}

SlideFiltersEntry* DecoderSlideFilter::decodeEntry(){
    bool connToFollow = decodeBool();
    double timestamp = decodeDouble();
    double value = decodeDouble();
    SlideFiltersEntry* recording = new SlideFiltersEntry(value, timestamp, connToFollow);
//    std::cout << "decodeEntry" << std::endl;
//    std::cout << "recording.connToFollow " << recording->connToFollow << std::endl;
//    std::cout << "recording.timestamp " << recording->timestamp << std::endl;
//    std::cout << "recording.value " << recording->value << std::endl;
    return recording;
}

SlideFiltersEntry* DecoderSlideFilter::getAt(int position){
    if (current_position < position){
        current_position = position;
        lastDecodedEntry = decodeEntry();
    }
    return lastDecodedEntry;
}


void DecoderSlideFilter::addValue(DataItem data_item){
    while (mask->isNoData()) {
        column->addNoData();
    }
    std::string value = Conversor::doubleToIntToString(data_item.value);
    column->addData(value);
}


// Calculate approximation data from model parameters
void DecoderSlideFilter::decompress(std::vector<int> x_coords_vector, int lastTimeStamp)
{
    SlideFiltersEntry slEntry1, slEntry2;
    DataItem inputEntry;

    mask->reset();
    current_position = -1;

    if (x_coords_vector.size() == 1){
        // TODO: decode an integer
        slEntry1 = *getAt(0);
        inputEntry.timestamp = slEntry1.timestamp;
        inputEntry.value = slEntry1.value;
        addValue(inputEntry);
        return;
    }

    int position = 0;
    double timeStamp = 0;
    int first_coord = x_coords_vector.at(0);

    Line* l = NULL;

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

            slEntry1 = *getAt(position);

            if (slEntry1.connToFollow)//Connected
            {
//                std::cout << "Connected" << std::endl;
                position++;
                slEntry2 = *getAt(position);

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
                addValue(inputEntry);
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
        addValue(inputEntry);
//        std::cout << "    add(inputEntry) = (" << inputEntry.timestamp << ", " << inputEntry.value << ") ********************************************************" << std::endl;
    }

    delete l;
}

#endif // MASK_MODE
