import os
import sys


def get_top_path(object_file_path,top_path_name):

    top_path = os.path.abspath(object_file_path)

    top_path = top_path.split(top_path_name)[0]
    top_path = os.path.join(top_path,top_path_name)

    sys.path.append(top_path)

    return top_path




