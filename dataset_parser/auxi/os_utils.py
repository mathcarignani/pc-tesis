import platform


class OSUtils(object):
    @staticmethod
    def ubuntu():
        return platform.system() == "Linux"

    @staticmethod
    def ios():
        return platform.system() == "Darwin"

    @staticmethod
    def datasets_csv_path():
        return OSUtils.project_path() + "/datasets-csv/"

    @staticmethod
    def git_path():
        return OSUtils.project_path() + "/pc-tesis"

    @staticmethod
    def cpp_project_path():
        return OSUtils.git_path() + "/cpp_project"

    @staticmethod
    def python_project_path():
        return OSUtils.git_path() + "/dataset_parser"

    @staticmethod
    def cpp_executable_path():
        if OSUtils.ios():
            return OSUtils.cpp_project_path() + "/cmake-build-debug/cpp_project"
        elif OSUtils.ubuntu():
            return OSUtils.cpp_project_path() + "/cmake-build-debug-ubuntu/cpp_project"
        else:
            raise SystemError("Invalid platform")

    @staticmethod
    def project_path():
        if OSUtils.ios():
            return "/Users/pablocerve/Documents/FING/Proyecto"
        elif OSUtils.ubuntu():
            return "/home/pablo/Documents/FING/Proyecto"
        else:
            raise SystemError("Invalid platform")
