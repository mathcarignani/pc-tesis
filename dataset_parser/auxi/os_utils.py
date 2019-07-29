import platform


# TODO: move these methods inside a class

def ubuntu():
    return platform.system() == "Linux"

def ios():
    return platform.system() == "Darwin"

def datasets_csv_path():
    return project_path() + "/datasets-csv/"

def git_path():
    return project_path() + "/pc-tesis"

def cpp_project_path():
    return git_path() + "/cpp_project"

def python_project_path():
    return git_path() + "/dataset_parser"

def cpp_executable_path():
    if ios():
        return cpp_project_path() + "/cmake-build-debug/cpp_project"
    elif ubuntu():
        return cpp_project_path() + "/cmake-build-debug-ubuntu/cpp_project"
    else:
        raise(StandardError, "Invalid platform")

def project_path():
    if ios():
        return "/Users/pablocerve/Documents/FING/Proyecto"
    elif ubuntu():
        return "/home/pablo/Documents/FING/Proyecto"
    else:
        raise(StandardError, "Invalid platform")
