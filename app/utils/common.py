import datetime
from decimal import Decimal
import gzip
import importlib
import inspect
from io import BufferedWriter
import json
import os
import pkgutil
import re
import sys
import traceback
import uuid
from boto3.dynamodb.types import Binary
from boto3.dynamodb.conditions import ConditionBase, AttributeBase
from app.system.config.constants import system_directories
from app.utils.logger import logger
from app.utils.path import get_project_root_dir

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        elif isinstance(o, Binary):
            try:
                return gzip.decompress(o.value).decode('utf-8')
            except Exception as e:
                logger.error(e)
                return '(Binary object)'
        elif isinstance(o, BufferedWriter):
            return '(BufferWriter object)'
        elif isinstance(o, ConditionBase):
            return o.get_expression()
        elif isinstance(o, AttributeBase):
            return o.name
        
        try:
            return super().default(o)
        except TypeError as e:
            logger.error(e)
            return 'Unsupported Type'

def split_list_into_batches(original_list, list_size):
    return [original_list[i:i + list_size] for i in range(0, len(original_list), list_size)]

def find_classes_inheriting_from(abstract_class, package_name = 'app'):
    classes = []
    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.walk_packages(package.__path__, prefix=package_name + '.'):
        if module_name not in set(sys.builtin_module_names):
            module = importlib.import_module(module_name)
            classes.extend(find_classes_inheriting_from_in_module(abstract_class, module))

    return deduplicate_classes(classes)

def find_classes_inheriting_from_in_module(abstract_class, module):
    classes = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, abstract_class) and obj != abstract_class and obj.__module__ == module.__name__:
            classes.append(obj)
    return classes

def import_module_from_path(file_path, module_name = None):
    module_name = module_name or file_path
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def find_classes_inheriting_from_in_root_dir(abstract_class):
    classes = []
    project_root_dir = get_project_root_dir()
    print(project_root_dir)
    print(system_directories)
    excluded_directories = [os.path.join(project_root_dir,d) for d in (system_directories + ['.'])]

    python_file_paths = []
    for root, _, files in os.walk(project_root_dir):
        if not any(root.startswith(p) for p in excluded_directories):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root,file)
                    python_file_paths.append(file_path)

    for fp in python_file_paths:
        with open(fp, 'r') as file:
            file_contents = file.read()
            if abstract_class.__name__ in file_contents:
                module = import_module_from_path(file_path)
                classes.extend(find_classes_inheriting_from_in_module(abstract_class, module))

    return deduplicate_classes(classes)

def deduplicate_classes(classes):
    deduplicated = []
    full_class_names = set()
    for c in classes:
        fcn = c.__module__ + '.' + c.__name__
        if fcn not in full_class_names:
            deduplicated.append(c)
            full_class_names.add(fcn)
    
    return deduplicated

def get_python_executable_path():
    return sys.executable

def get_exception_detail(e: Exception):
    return [f"{e.__class__.__module__}.{e.__class__.__name__}: {e}"] + traceback.format_list(traceback.extract_tb(e.__traceback__))

def camel_to_snake(camel_case_str):
    pattern = re.compile(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')
    snake_case_str = pattern.sub('_', camel_case_str)
    return snake_case_str.lower()

def snake_to_camel(snake_case_str):
    components = snake_case_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def remove_none_values(dict):
    return {k:v for k,v in dict.items() if v is not None}