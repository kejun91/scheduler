import os
from pathlib import Path
import threading

lock = threading.Lock()

def get_project_root_dir():
    '''
    root_dir/app/utils/path.py
    '''
    return Path(__file__).parent.parent.parent.resolve()

def get_data_dir_path(*path_segments):
    return get_dir_path('data', *path_segments)

def get_data_file_path(*path_segments, create_file = False):
    return get_file_path('data', *path_segments)

def get_output_dir_path(*path_segments):
    return get_dir_path('output', *path_segments)

def get_output_file_path(*path_segments, create_file = False):
    return get_file_path('output', *path_segments, create_file = create_file)

def get_dir_path(*path_segments):
    dir_path = os.path.join(get_project_root_dir(), *path_segments)
    with lock:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    return dir_path

def get_file_path(*path_segments, create_file = False):
    file_path = os.path.join(get_project_root_dir(), *path_segments)
    dir_path = get_dir_path(*path_segments[:-1])
    with lock:
        if not os.path.exists(file_path) and create_file:
            with open(file_path, 'w') as f:
                pass
    return file_path