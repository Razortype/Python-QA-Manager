import re
import generator.constant as c
import time
import re

def func_exists(val_type,func_dict):
    return val_type not in func_dict.keys()

def find_parens(s):
    toret = {}
    pstack = []
    for i, c in enumerate(s):
        if c == '(':
            pstack.append(i)
        elif c == ')':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i
    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))
    return toret

def seperate_values(pattern, indexs):
    first_value, *tail = sorted(indexs.items())
    func_type = pattern[0:first_value[0]]
    return (func_type, first_value, tail)

def convert_dict_format(values):
    new_vals = []
    for value in values:
        meta = {}
        for val in value.split(","):
            param_key, param_val = val.split(":")
            meta[param_key] = eval(param_val)
        new_vals.append(meta)
    return new_vals

def list_dict_args(value_meta):
    new_meta = {'type':value_meta.get('type')}
    if value_meta.get("type") == "list":
        first, second = value_meta.get("params")
        new_meta['params'] = second
        new_meta['params']['args'] = first
        
    elif value_meta.get("type") == "dict":
        first, second, third = value_meta.get("params")
        new_meta['params'] = third
        new_meta['params']['key_args'] = first
        new_meta['params']['value_args'] = second

    return new_meta