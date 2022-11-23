
def calculate_percent(results):
    check_res = [res[-1] for res in results]
    total = len(check_res)
    valid = sum([1 for passed in check_res if passed])
    percen = round(valid / total * 100, 2)
    return percen

def max_digit_len(array):
    return len(str(len(array)))

def list_to_str(lst):
    if not isinstance(lst, (list, dict, set)): return str(lst)
    return ", ".join(map(str,lst))

def get_reqs_params(data):
    func_name = data.get("name")
    results = data.get("result")
    elapsed_time = data.get("elapsed")
    percentage = calculate_percent(results)
    return func_name, percentage, elapsed_time, results

def result_filter(results):
    return [i for i in results if not i[-1]]

def check_passed(results):
    if not results: return False
    return all([i[-1] for i in results])

def convert_table_valid(*args):
    return [list_to_str(i) for i in args]