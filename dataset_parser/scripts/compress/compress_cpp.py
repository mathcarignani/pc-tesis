import os
import subprocess
from auxi.os_utils import OSUtils
from auxi.time_track import TimeTrack
from scripts.utils import str_to_int
from scripts.compress.experiments_utils import ExperimentsUtils

class CompressCPP:
    PRINT_MODE = False

    @classmethod
    def code_decode_cpp(cls, args):
        coder_name, header_bits, column_bits, column_mask_bits = cls.code_cpp(args)
        cls.decode_cpp(args)
        return [coder_name, header_bits, column_bits, column_mask_bits]

    @classmethod
    def code_cpp(cls, args):
        time_track = TimeTrack()
        args.code_cpp()
        exe_str = OSUtils.cpp_executable_path() + " c"
        exe_str += " " + args.input_path + " " + args.input_filename
        exe_str += " " + args.output_path + " " + args.compressed_filename
        exe_str += " " + cls._coder_params(args)
        header_bits, column_bits, column_mask_bits = cls._execute(exe_str)
        print(args.input_filename, "code_c++ - elapsed time =", time_track.elapsed(2), "seconds")
        return [args.coder_name, header_bits, column_bits, column_mask_bits]

    @classmethod
    def decode_cpp(cls, args):
        time_track = TimeTrack()
        args.decode_cpp()
        exe_str = OSUtils.cpp_executable_path() + " d"
        exe_str += " " + args.output_path + " " + args.compressed_filename
        exe_str += " " + args.output_path + " " + args.deco_filename
        cls._execute(exe_str)
        print(args.compressed_filename, "decode_c++ - elapsed time =", time_track.elapsed(2), "seconds")

    @classmethod
    def _execute(cls, exe_str):
        cls._print_exe(exe_str)
        header_bits, column_bits, column_mask_bits = 0, [], []
        if cls.PRINT_MODE:
            os.system(exe_str)
            cls._print_end()
            return header_bits, column_bits, column_mask_bits

        sub = subprocess.Popen(exe_str.split(" "), stdout=subprocess.PIPE)
        stdout = sub.communicate()[0]
        stdout_list = stdout.split("\n")
        for line in stdout_list:
            if "header_bits" in line:
                header_bits = str_to_int(line)
            elif "total_mask_bits" in line:
                bits = str_to_int(line)
                column_mask_bits.append(bits)
            elif "total_bits" in line:
                bits = str_to_int(line)
                column_bits.append(bits)
        cls._print_end()
        return header_bits, column_bits, column_mask_bits

    @classmethod
    def _coder_params(cls, args):
        if args.coder_name not in ExperimentsUtils.CODERS:
            raise(KeyError, "ERROR: Invalid coder name " + args.coder_name)

        if args.coder_name == "CoderBase":
            return "CoderBase"

        error_thresholds = " ".join(str(i) for i in args.coder_params['error_threshold'])
        string = args.coder_name + " " + str(args.coder_params['window_size']) + " " + error_thresholds
        return string

    @staticmethod
    def _print_exe(exe_str):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> C++")
        print(exe_str)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> C++")

    @staticmethod
    def _print_end():
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<< C++")
