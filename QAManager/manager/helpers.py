import json, sys, inspect, builtins
import importlib.util
from click import option
from pick import pick
import re

def load_json(file_dir):
    with open(file_dir, "r") as f:
        app_data = json.loads(f.read())
    return app_data

def deploy_json(file_dir, data):
    with open(file_dir, "w") as f:
        json.dump(data, f, indent=4)

def clean_lines(lines):
    return [line.replace("\n","") for line in lines]

def seperate_vars(string, param):
    return list((eval(i),type(eval(i)).__name__) for i in string.split(param))

def load_file(name,dir):
    spec = importlib.util.spec_from_file_location(name,dir)
    foo = importlib.util.module_from_spec(spec)
    sys.modules[name] = foo
    spec.loader.exec_module(foo)
    return foo

def clear_invalid_funcs(func_list):
    return [i for i in func_list if not i.startswith("__") and not i.endswith("__")]

def path_to_name(path):
    return path.replace("//","/").split("/")[-1]

def get_func_attrs(func):
    start, end = span_of_function(func)
    return {
        'name': func.__name__,
        'variables': inspect.getfullargspec(func)[0],
        'defaults': func.__defaults__,
        'start':start,
        'end':end,
        'function': func
    }
    
def span_of_function(func):
  start = func.__code__.co_firstlineno
  end = start + sum(line_increment for i, line_increment in enumerate(func.__code__.co_lnotab) if i % 2)
  return start, end

def only_args(lst):
    if lst:
        res_lst = []
        for row in lst:
            res_lst.append([i[0] for i in row])
        return res_lst
    return []

def correction(result):
    if isinstance(result, (tuple, set, dict, list)):
        return list(result)
    return [result]

def get_exact_part(data_dict, path_list):
    for path in path_list:
        data_dict = data_dict.get(path)
    return data_dict

def value_type_func(value):
    return getattr(builtins, type(value).__name__)

def pick_archive(archives):
    title = "Select an archived file from list : "
    options = [f"{key:<15} : {value:>5}"  for key,value in archives.items()]
    archive, index = pick(options, title)
    return list(archives.values())[index]

def replace_archive(file_dir, cases_dir):
    
    with open(file_dir, "r") as selected_file:
        selected_file_data = selected_file.read()

    with open(cases_dir, "w") as cases_file:
        cases_file.write(selected_file_data)

def add_quotest_to_string(value):
    if type(value).__name__ == "str":
        return f"\"{value}\""
    return str(value)

def add_quotest_to_list(input_list):
    return [extract_white_spaces(add_quotest_to_string(i)) for i in input_list]

# def validate_func(a, b):
#     print(a)
#     print(b)
#     return True

def extract_white_spaces(var):
    parts = re.split(r"""("[^"]*"|'[^']*')""", var)
    parts[::2] = map(lambda s: "".join(s.split()), parts[::2]) # outside quotes
    return "".join(parts)

def save_to_archive(archive_dir, file_name, file_data):
    
    with open(archive_dir+file_name, "w") as f:
        f.write(file_data)