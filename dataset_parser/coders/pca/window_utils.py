

#
# This method is used to check the constraint violation in the following compression algorithms:  PCA, APCA, PWLH
# PRE:
# (1) min_val and max_val are integers
# (2) min_val <= max_val
#
def valid_threshold(min_val, max_val, error_threshold):
    min_val_aux = min_val + abs(min_val)  # >= 0
    max_val_aux = max_val + abs(min_val)  # >= 0
    width = max_val_aux - min_val_aux  # >= 0
    return valid_width(width, error_threshold)


def valid_width(width, error_threshold):
    return False if width > 2*error_threshold else True
