import os
import time
import subprocess


EXE = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project/cmake-build-debug/cpp_project"


def execute(exe_str):
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>> C++"
    print exe_str
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>> C++"
    # os.system(exe_str)
    column_bits = []
    sub = subprocess.Popen(exe_str.split(" "), stdout=subprocess.PIPE)
    stdout = sub.communicate()[0]
    stdout_list = stdout.split("\n")
    for line in stdout_list:
        if "total_bits" in line:
            print line
            bits = int(line.replace("total_bits ", ""))
            column_bits.append(bits)
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<< C++"
    return column_bits


def code_cpp(args):
    start_time = time.time()
    args.code_cpp()
    exe_str = EXE + " c"
    exe_str += " " + args.input_path + " " + args.input_filename
    exe_str += " " + args.output_path + " " + args.compressed_filename
    exe_str += " " + coder_params(args)
    column_bits = execute(exe_str)
    elapsed_time = time.time() - start_time
    print args.input_filename, "code_c++ - elapsed time =", round(elapsed_time, 2), "seconds"
    return [args.coder_name, column_bits]


def decode_cpp(args):
    start_time = time.time()
    args.decode_cpp()
    exe_str = EXE + " d"
    exe_str += " " + args.output_path + " " + args.compressed_filename
    exe_str += " " + args.output_path + " " + args.deco_filename
    exe_str += " " + coder_params(args)
    execute(exe_str)
    elapsed_time = time.time() - start_time
    print args.compressed_filename, "decode_c++ - elapsed time =", round(elapsed_time, 2), "seconds"


def coder_params(args):
    if args.coder_name == "CoderBasic":
        return "CoderBasic"
    elif args.coder_name == "CoderPCA":
        error_thresholds = " ".join(str(i) for i in args.coder_params['error_threshold'])
        string = "CoderPCA " + str(args.coder_params['fixed_window_size']) + " " + error_thresholds
        return string
    elif args.coder_name == "CoderAPCA":
        error_thresholds = " ".join(str(i) for i in args.coder_params['error_threshold'])
        string = "CoderAPCA " + str(args.coder_params['max_window_size']) + " " + error_thresholds
        return string
    elif args.coder_name == "CoderCA":
        error_thresholds = " ".join(str(i) for i in args.coder_params['error_threshold'])
        string = "CoderCA " + str(args.coder_params['max_window_size']) + " " + error_thresholds
        return string
    elif args.coder_name == "CoderPWLH":
        error_thresholds = " ".join(str(i) for i in args.coder_params['error_threshold'])
        string = "CoderPWLH " + str(args.coder_params['max_window_size']) + " " + error_thresholds
        return string
    elif args.coder_name == "CoderPWLHint":
        error_thresholds = " ".join(str(i) for i in args.coder_params['error_threshold'])
        string = "CoderPWLHint " + str(args.coder_params['max_window_size']) + " " + error_thresholds
        return string


def code_decode_cpp(args):
    coder_name, column_bits = code_cpp(args)
    decode_cpp(args)
    return [coder_name, column_bits]
