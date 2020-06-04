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
        args.code_cpp()
        exe_str = cls._code_cpp_exe_str(args)

        time_track = TimeTrack()
        header_bits, column_bits, column_mask_bits = cls._execute(exe_str)
        elapsed = time_track.elapsed(2)

        print(args.input_filename, "code_c++ - elapsed time =", elapsed, "seconds")
        return [args.coder_name, header_bits, column_bits, column_mask_bits]

    @classmethod
    def decode_cpp(cls, args):
        args.decode_cpp()
        exe_str = cls._decode_cpp_exe_str(args)

        time_track = TimeTrack()
        cls._execute(exe_str)
        elapsed = time_track.elapsed(2)

        print(args.compressed_filename, "decode_c++ - elapsed time =", elapsed, "seconds")

    ####################################################################################################################

    @classmethod
    def _code_cpp_exe_str(cls, args):
        exe_str = cls._executable_path(args.coder_name)
        exe_str += " c"
        exe_str += " " + args.input_path + "/" + args.input_filename
        exe_str += " " + args.output_path + "/" + args.compressed_filename
        exe_str += " " + cls._coder_params(args)
        return exe_str

    @classmethod
    def _decode_cpp_exe_str(cls, args):
        exe_str = cls._executable_path(args.coder_name)
        exe_str += " d"
        exe_str += " " + args.output_path + "/" + args.compressed_filename
        exe_str += " " + args.output_path + "/" + args.deco_filename
        return exe_str

    @classmethod
    def _execute(cls, exe_str):
        cls._print_begin(exe_str)
        header_bits, column_bits, column_mask_bits = 0, [], []
        if cls.PRINT_MODE:
            os.system(exe_str)
            cls._print_end()
            return header_bits, column_bits, column_mask_bits

        result = subprocess.run(exe_str.split(" "), stdout=subprocess.PIPE)
        stdout = result.stdout.decode('utf-8')
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
        window_size = str(args.coder_params['window_size'])
        string = args.coder_name + " " + window_size + " " + error_thresholds
        return string

    @staticmethod
    def _executable_path(coder_name):
        exe_str = OSUtils.cpp_executable_path()
        mask_mode = 0 if coder_name == "CoderBase" else ExperimentsUtils.MASK_MODE
        mask_mode = str(mask_mode)
        exe_str += "_" + mask_mode + " " + mask_mode
        return exe_str

    @staticmethod
    def _print_begin(exe_str):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> C++")
        print(exe_str)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> C++")

    @staticmethod
    def _print_end():
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<< C++")
