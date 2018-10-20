
from auxi.dataset_utils import DatasetUtils

# TODO: improve method
def gamps_group_thresholds(thresholds_hash, dataset_name):
    du = DatasetUtils('code')
    data_columns_group_count = len(du.constants['alphabets_dictionary'][dataset_name]) - 1  # minus time delta
    print "data_columns_group_count = " + str(data_columns_group_count)
    for percentage, thresholds_array in thresholds_hash.iteritems():
        print "percentage " + str(percentage)
        new_thresholds_array = [thresholds_array.pop(0)]  # time delta error threshold, is always 0

        for group_id in range(data_columns_group_count):
            group_thresholds = []
            for col_index, threshold in enumerate(thresholds_array):
                if data_columns_group_count == 1 or ((col_index % data_columns_group_count) == group_id):
                    group_thresholds.append(threshold)

            group_threshold = "N"
            for threshold in group_thresholds:
                if group_threshold == "N" or (threshold != "N" and threshold < group_threshold):
                    group_threshold = threshold
            print group_threshold
            new_thresholds_array.append(group_threshold)

        thresholds_hash[percentage] = new_thresholds_array
    return thresholds_hash
