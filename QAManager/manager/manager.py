import time, os

import manager.helpers as h
import manager.constant as c

class Manager:
    
    def __init__(self, main_dir):
        self.main_dir = main_dir
        self.app_data_dir = self.get_full_path(c.Vars.DATA_JSON_DIR)
        self.app_data = {}

    def get_data(self):
        if not self.app_data:
            self.app_data = h.load_json(self.app_data_dir)
        return self.app_data

    def deploy_data(self, data={}):
        if data:
            h.deploy_json(data)

    def get_full_path(self, path):
        return path.replace(c.Vars.MAIN_DIR_SPLIT, str(self.main_dir))

class DeployManager(Manager):
    
    def __init__(self, main_dir):
        super().__init__(main_dir)

        self.input_lst = []
        self.output_lst = []
        self.pattern = ""

    def load_case(self):
        with open(self.get_full_path(self.get_data()["Deploy"]["case-dir"]), "r") as case_file:
            lines = case_file.read().split(c.Vars.TEST_SPLIT)

        for line in lines:
            ipt, res = line.split(c.Vars.IO_CASE_SPLIT)

            self.input_lst.append(h.seperate_vars(ipt, c.Vars.VARS_SPLIT))
            self.output_lst.append(h.seperate_vars(res, c.Vars.VARS_SPLIT))
            self.pattern = [row[1] for row in self.input_lst[0]]

    def get_pattern(self, string=False):
        if string:
            return f"({', '.join(self.pattern)})"
        return self.pattern

    def get_case_amount(self):
        return len(self.input_lst)
    
    def deploy_testcase(self, case_name):
        archives = self.get_data()["Create"]["archive-items"]

        if case_name is None:
            selected = h.pick_archive(archives)
        else:
            selected = archives.get(case_name, None)

        if selected is not None:
            archive_dir = self.get_full_path(self.get_data()["Create"]["archive-dir"])+selected
            h.replace_archive(archive_dir, self.get_full_path(self.get_data()["Deploy"]["case-dir"]))
            print(f'Cases file replaced with "{selected}" file successfully.')
        else:
            print(f"Case name not found! ({case_name})")

    def save_archive(self, results):
        
        if "y" == input("Want to save as archive? (Y/n) : ").lower():
            archives = [i for i in self.get_data()["Create"]["archive-items"]]
            name = input("Enter file name : ")
            if name not in archives:
                file_name =  "/" + name.replace(" ", "_").lower() + ".txt"
                archive_dir = self.get_full_path(self.get_data()["Create"]["archive-dir"])
    
                data = self.get_data()
                data["Create"]["archive-items"][name] = file_name
                
                h.deploy_json(self.get_full_path(c.Vars.DATA_JSON_DIR), data)
                h.save_to_archive(archive_dir, file_name, c.Vars.TEST_SPLIT.join(results))

class CreateManager(Manager):
 
    def __init__(self, main_dir, random_generator):
        super().__init__(main_dir)
        self.random_generator = random_generator
        self.pattern = None
        self.process_func = None
        self.generated_variables = []
        self.generated_rows = []

    def deploy_pattern(self, pattern):
        self.pattern = pattern

    def deploy_process_func(self, func):
        self.process_func = func

    def evaluate_pattern(self):
        self.generated_variables = []
        variable_columns = self.pattern.split(c.Vars.VARS_SPLIT)
        for variable in variable_columns:
            self.generated_variables.append(self.random_generator.eval_pattern(variable))

    def process_func_results(self, amount):
        for _ in range(amount):
            self.evaluate_pattern()
            self.generated_rows.append((self.generated_variables, self.process_func.get("function")(*self.generated_variables)))
            self.generated_variables = []

    def conver_to_archive(self):
        results = []
        for row in self.generated_rows:
            input_value, output_value = row
            input_value = h.add_quotest_to_list(input_value)
            results.append(c.Vars.VARS_SPLIT.join(input_value)+c.Vars.IO_CASE_SPLIT+h.add_quotest_to_string(output_value))
        return results

class TestManager(Manager):
    
    def __init__(self, main_dir):
        super().__init__(main_dir)
        self.funcs = {}

    def run_all(self, input_lst, output_lst):

        for file_name in self.funcs.keys():
            for index, func_data in enumerate(self.funcs[file_name]):
                func_result = []
                elapsed = 0

                func = func_data['function']
                input_args, output_args = h.only_args(input_lst), h.only_args(output_lst)

                try:
                    func_result, elapsed = self.run(func, input_args, output_args)
                except Exception as e:
                    print(e)

                self.funcs[file_name][index]['elapsed'] = elapsed
                self.funcs[file_name][index]['result'] = func_result

    def process(self, func, input_lst):
        results = [func(*args) for args in input_lst]
        return results

    def run(self, func, input_lst, output_lst):
        results = []
        start = time.time()
        for index ,args in enumerate(input_lst,1):
            expected = output_lst[index-1]
            func_res = h.correction(func(*args))
            results.append((index, args, expected, func_res, self.check_eq(expected, func_res)))
        end = time.time()
        return results, end-start

    def check_eq(self, expected, result):
        if len(expected) != len(result): return False
        return all([expected[i]==result[i] for i in range(len(expected))])

    def load_funcs(self, func_names="all##"):
        paths = [self.get_full_path(dir) for dir in self.get_data()["Test"]["funcs-dirs"]] ## get full path to the function file
        files = [h.load_file(h.path_to_name(path),path) for path in paths if os.path.exists(path)]
        
        for file in files:
            func_lst = []
            valid_funcs = h.clear_invalid_funcs(dir(file))
            for func in valid_funcs:
                func_lst.append(h.get_func_attrs(getattr(file, func)))
            func_lst.sort(key=lambda obj: obj['start'])
            self.funcs[file.__name__] = func_lst
        
        if func_names != "all##":
            self.clear_invalid_funcs(func_names.split(","))

    def clear_invalid_funcs(self, reqs):
        for file_name, file_data in self.funcs.items():
            self.funcs[file_name] = [data for data in file_data if data['name'] in reqs]

    def get_func_by_name(self, name):
        for file_value in self.funcs.values():
            if file_value:
                for func in file_value:
                    if func.get("name") == name:
                        return func
        return None