import os
import time
import subprocess
from auxi.os_utils import cpp_executable_path

EXE = cpp_executable_path()


def execute(exe_str):
    print_mode = False
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>> C++"
    print exe_str
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>> C++"
    column_bits = []
    column_mask_bits = []
    if print_mode:
        os.system(exe_str)
        print "<<<<<<<<<<<<<<<<<<<<<<<<<<<< C++"
        return column_bits, column_mask_bits

    sub = subprocess.Popen(exe_str.split(" "), stdout=subprocess.PIPE)
    stdout = sub.communicate()[0]
    stdout_list = stdout.split("\n")
    for line in stdout_list:
        if "total_bits" in line:
            print line
            bits = int(line.replace("total_bits ", ""))
            column_bits.append(bits)
        elif "total_mask_bits" in line:
            print line
            bits = int(line.replace("total_mask_bits ", ""))
            column_mask_bits.append(bits)
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<< C++"
    return column_bits, column_mask_bits


def code_cpp(args):
    start_time = time.time()
    args.code_cpp()
    exe_str = EXE + " c"
    exe_str += " " + args.input_path + " " + args.input_filename
    exe_str += " " + args.output_path + " " + args.compressed_filename
    exe_str += " " + coder_params(args)
    column_bits, column_mask_bits = execute(exe_str)
    elapsed_time = time.time() - start_time
    print args.input_filename, "code_c++ - elapsed time =", round(elapsed_time, 2), "seconds"
    return [args.coder_name, column_bits, column_mask_bits]


def decode_cpp(args):
    start_time = time.time()
    args.decode_cpp()
    exe_str = EXE + " d"
    exe_str += " " + args.output_path + " " + args.compressed_filename
    exe_str += " " + args.output_path + " " + args.deco_filename
    execute(exe_str)
    elapsed_time = time.time() - start_time
    print args.compressed_filename, "decode_c++ - elapsed time =", round(elapsed_time, 2), "seconds"


def coder_params(args):
    coder_names = ["CoderBasic", "CoderPCA", "CoderAPCA", "CoderPWLH",
                   "CoderPWLHInt", "CoderCA", "CoderSF", "CoderFR", "CoderGAMPS"]

    if args.coder_name not in coder_names:
        print args.coder_name
        raise(StandardError, "ERROR: Invalid coder name")

    if args.coder_name == "CoderBasic":
        return "CoderBasic"
    else:
        error_thresholds = " ".join(str(i) for i in args.coder_params['error_threshold'])
        string = args.coder_name + " " + str(args.coder_params['window_size']) + " " + error_thresholds
        return string


def code_decode_cpp(args):
    coder_name, column_bits, column_mask_bits = code_cpp(args)
    decode_cpp(args)
    return [coder_name, column_bits, column_mask_bits]
