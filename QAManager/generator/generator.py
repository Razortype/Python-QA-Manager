from random import randint, choice, uniform
import string

import generator.helpers as h
import generator.constant as c

class RandomGenerator:

    num_list = ["0","1","2","3","4","5","6","7","8","9"]

    @classmethod
    def number(cls, s: int=5, e: int=10, length: int=5, inval: bool=False, dig: bool=False) -> int:
        # Expected Cases --
        if not inval and not dig: return -999 # non-interval and non-digit
        if s>e: return -999 # start interval bigger than end interval
        if inval and dig: return -999 # both interval and digit True
        if length <= 0: return -999 # non-digit declared

        if inval:
           random_number = randint(s, e)
           return random_number
        elif dig:
            num_str: str = ''
            for i in range(1, length+1):
                start_index = 0 if i != 1 else 1 # numbers can't start with zero
                # choice start from first interval if it is not first digit of number
                num_str += cls.num_list[choice(range(start_index,len(cls.num_list)))] 
            return int(num_str)

    @classmethod
    def string(cls, s: int=5, e: int=10, length: int=5, random: bool=False) -> str:
        # Expected Cases --
        if s>e: return "None"
        if e-s>=255: return "None"
        if length <= 0: return "None"
        if length >= 255: return "None"

        word: str = ""
        if random:
            rand_lenght = randint(s,e)
            word = ''.join((choice(string.ascii_lowercase) for _ in range(rand_lenght)))
        else:
            word = ''.join((choice(string.ascii_lowercase) for _ in range(length)))
        return word

    @classmethod
    def boolean(cls, number: bool=False) -> bool:
        val = randint(0,1)
        if number:
            return val
        return bool(val)

    @classmethod
    def double(cls, s: float=5.0, e: float=25.0, rnd: int=None) -> float:
        if rnd < 0: return -999.0
        
        rand_double = uniform(s, e)
        if rnd is not None:
            return round(rand_double, rnd)
        return rand_double

    @classmethod
    def _list(cls, s: int= 1, e: int=5, times: int=5, order: bool=False, value_type: str=None, args: dict={}) -> list:
        if value_type is None: return []
        if h.func_exists(value_type, cls.get_func()): return []
        if s>e: return []
        if times <= 0: return []

        if order and value_type=="num":
            return [cls.number(s=i,e=i,inval=True) for i in range(s,e+1)]
        func = cls.get_func(value_type)
        return [func(**args) for _ in range(times)]

    @classmethod
    def _dict(cls, times: int=5, key_type: str=None, value_type: str=None, key_args: dict={}, value_args: dict={}) -> dict:
        if times <= 0: return {}
        if key_type is None or value_type is None: return {}
        if h.func_exists(key_type, cls.get_func()) or h.func_exists(value_type, cls.get_func()): return {}
        
        key_func = cls.get_func(key_type)
        value_func = cls.get_func(value_type)
        return {key_func(**key_args):value_func(**value_args) for _ in range(times)}

    @classmethod
    def get_func(cls, name=None):
        func_dict = {
            c.GeneratedFunction.NUMBER : cls.number,
            c.GeneratedFunction.STRING : cls.string,
            c.GeneratedFunction.BOOL   : cls.boolean,
            c.GeneratedFunction.DOUBLE : cls.double,
            c.GeneratedFunction.LIST   : cls._list,
            c.GeneratedFunction.DICT   : cls._dict,
            c.GeneratedFunction.NONE   : lambda : None
        }
        if name:
            return func_dict.get(name, None)
        return func_dict

    @classmethod
    def fetch_variables(cls, pattern):
        value_meta = {}

        indexs = h.find_parens(pattern)
        value_meta["type"], first_value, tail = h.seperate_values(pattern, indexs)
        
        if value_meta.get("type") not in cls.get_func().keys(): exit()

        if value_meta.get("type") in ["list", "dict"]:
            values = [pattern[s+1:e] for s,e in tail]
        else:
            values = [pattern[first_value[0]+1:first_value[1]]]
        
        value_meta["params"] = h.convert_dict_format(values)

        if value_meta.get("type") in ["dict", "list"]:
            value_meta = h.list_dict_args(value_meta)
        else:
            value_meta["params"] = eval(str(value_meta["params"])[1:-1])
        
        return value_meta

    @classmethod
    def eval_pattern(cls, pattern):
        if pattern == "NONE": return cls.get_func(pattern)()
        func_meta = cls.fetch_variables(pattern)
        func = cls.get_func(func_meta.get('type'))
        return func(**func_meta.get('params'))