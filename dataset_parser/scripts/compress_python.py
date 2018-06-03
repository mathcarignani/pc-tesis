import time
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter


def code_python(args):
    start_time = time.time()
    args.code_python()
    input_csv = CSVReader(args.input_path, args.input_filename, True)
    c = args.coder(input_csv, args.output_path, args.compressed_filename, args.coder_params)
    c.code_file()
    c.close()
    coder_info = c.get_info()
    columns_bits = [column_code.total_bits for column_code in c.dataset.column_code_array]
    print columns_bits
    elapsed_time = time.time() - start_time
    print args.input_filename, "code_python - elapsed time =", round(elapsed_time, 2), "seconds"
    return [coder_info, columns_bits]


def decode_python(args):
    start_time = time.time()
    args.decode_python()
    output_csv = CSVWriter(args.output_path, args.deco_filename)
    d = args.decoder(args.output_path, args.compressed_filename, output_csv, args.coder_params)
    try:
        d.decode_file()
    except AssertionError as e:
        if e == "Reached EOF.":
            print "ERROR: Reached End Of File."
    d.close()
    elapsed_time = time.time() - start_time
    print args.compressed_filename, "decode_python - elapsed time =", round(elapsed_time, 2), "seconds"


def code_decode_python(args):
    coder_info, columns_bits = code_python(args)
    decode_python(args)
    return [coder_info, columns_bits]