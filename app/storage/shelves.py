import shelve
import threading
from app.utils.path import get_data_file_path

lock = threading.Lock()
class Shelves:
    def __init__(self, shelf_name='default'):
        dir_paths = ()
        if '.' in shelf_name:
            segments = shelf_name.split('.')
            dir_paths = tuple(segments[:-1])
            shelf_name = segments[-1]
        self.shelf_path = get_data_file_path('shelves',*dir_paths, shelf_name)

    def set_value(self, key, value):
        with lock:
            with shelve.open(self.shelf_path) as shelf:
                shelf[key] = value

    def get_value(self, key):
        with lock:
            with shelve.open(self.shelf_path) as shelf:
                return shelf.get(key)
        
    def get_keys(self):
        with lock:
            with shelve.open(self.shelf_path) as shelf:
                return list(shelf.keys())