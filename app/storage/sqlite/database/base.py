from abc import ABC, abstractmethod
from app.storage.sqlite.database.connection import sqlite_connection
from app.utils.path import get_data_file_path


class AbstractDB(ABC):
    def __init__(self, database_name='default', dir_paths = ()):
        dir_paths = ()
        if '.' in database_name:
            segments = database_name.split('.')
            dir_paths = tuple(segments[:-1])
            database_name = segments[-1]
        self.database_path = get_data_file_path('database',*dir_paths, database_name + '.db')
    
    @abstractmethod
    def execute_select_query(self, select_query_string, parameters = ()):
        pass

    @abstractmethod
    def execute_query(self, query, parameters = ()):
        pass

    @abstractmethod
    def execute_batch_modify_query(self, modify_query, parameters):
        pass

    def is_table_existed(self, table_name):
        with sqlite_connection(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            result = cursor.fetchone()
            return True if result else False