import os

EXE = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project/cmake-build-debug/cpp_project"


def execute(exe_str):
    print ">>>>>>>>>>>>>>>>>> C++"
    os.system(exe_str)
    print "<<<<<<<<<<<<<<<<<< C++"


def code_cpp(args):
    args.code_cpp()
    exe_str = EXE + " c"
    exe_str += " " + args.input_path + " " + args.input_filename
    exe_str += " " + args.output_path + " " + args.compressed_filename
    exe_str += " CoderBasic"
    execute(exe_str)


def decode_cpp(args):
    args.decode_cpp()
    exe_str = EXE + " d"
    exe_str += " " + args.output_path + " " + args.compressed_filename
    exe_str += " " + args.output_path + " " + args.deco_filename
    exe_str += " CoderBasic"
    execute(exe_str)


def code_decode_cpp(args):
    code_cpp(args)
    decode_cpp(args)
