import os


def csv_files_filenames(input_path, endswith=".csv"):
    input_filenames = os.listdir(input_path)
    input_filenames = [f for f in input_filenames if os.path.isfile(os.path.join(input_path, f))]
    input_filenames = [f for f in input_filenames if f.endswith(endswith)]
    return input_filenames


def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

