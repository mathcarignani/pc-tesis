import os
import time


EXE = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project/cmake-build-debug/cpp_project"


def execute(exe_str):
    print exe_str
    print ">>>>>>>>>>>>>>>>>> C++"
    os.system(exe_str)
    print "<<<<<<<<<<<<<<<<<< C++"


def code_cpp(args):
    start_time = time.time()
    args.code_cpp()
    exe_str = EXE + " c"
    exe_str += " " + args.input_path + " " + args.input_filename
    exe_str += " " + args.output_path + " " + args.compressed_filename
    exe_str += " " + coder_params(args)
    execute(exe_str)
    elapsed_time = time.time() - start_time
    print args.input_filename, "code_c++ - elapsed time =", round(elapsed_time, 2), "seconds"


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


def code_decode_cpp(args):
    code_cpp(args)
    decode_cpp(args)
