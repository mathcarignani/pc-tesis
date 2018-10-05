import platform


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

def project_path():
    if ios():
        return "/Users/pablocerve/Documents/FING/Proyecto"
    elif ubuntu():
        return "/home/pablo/Documents/FING/Proyecto"
    else:
        raise(StandardError, "Invalid platform")
