from rich.table import Table
from rich.console import Console
from rich import box
import json
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.web import JsonLexer

import display.helpers as h
import display.constant as c

import manager.constant as m_c

class Display:
    
    console = Console()

    @classmethod
    def print_funcs(cls, data, detailed: bool=False):
        for file_section, file_data in data.items():
            cls.console.print(c.Fonts.func_table_title.format(f"{file_section}"),
                                c.Fonts.func_table_default.format("file Section ~~"))
            if file_data:
                if not detailed:
                    cls.print_func_table(file_data)
                else:
                    cls.print_func_table_detail(file_data)
            else:
                cls.console.print(c.Fonts.func_table_error.format("No function(s) is specified in file!"))

    @classmethod
    def print_func_table(cls, file_data):
        
        table = Table(show_header=True, header_style="bold blue", box=box.MINIMAL_HEAVY_HEAD)
        table.add_column("#", style="dim", width=len(file_data), justify="center")
        table.add_column("Name", min_width=15)
        table.add_column("Variable(s)", min_width=15)
        table.add_column("Start", min_width=5, justify="center")

        for index, func in enumerate(file_data, 1):
            index, name, variables, start = h.convert_table_valid(index, func['name'], func['variables'], func['start'])
            table.add_row(
                            index,
                            c.Fonts.func_table_name.format(name),
                            variables,
                            c.Fonts.func_table_index.format(start)
                        )

        cls.console.print(table)

    @classmethod
    def print_func_table_detail(cls, file_data):
        
        table = Table(show_header=True, header_style="bold blue", box=box.MINIMAL_HEAVY_HEAD)
        table.add_column("#", style="dim", width=len(file_data), justify="center")
        table.add_column("Name", min_width=15)
        table.add_column("Variable(s)", min_width=15)
        table.add_column("Defult(s)", min_width=15)
        table.add_column("Start", min_width=5, justify="center")
        table.add_column("End[red](?)[/red]", min_width=5, justify="center")
        table.add_column("Address", min_width=10)

        for index, func in enumerate(file_data, 1):
            index, name, variables, defaults, start, end, address = h.convert_table_valid(index, func['name'], func['variables'], func['defaults'], func['start'], func['end'], func['function'])
            table.add_row(
                            index,
                            c.Fonts.func_table_name.format(name),
                            variables,
                            defaults,
                            c.Fonts.func_table_index.format(start),
                            c.Fonts.func_table_index.format(end),
                            c.Fonts.func_table_default.format(address)
                        )

        cls.console.print(table)

    @classmethod
    def print_results(cls, result_data: dict={}, show_table: bool=True, only_non_valids: bool=False, pattern:str = ""):
        for file_section in result_data.values():
            for data in file_section:
                
                if not data['result']: continue
                func_name, percentage, elapsed_time, results = h.get_reqs_params(data)

                cls.console.print(c.Fonts.table_title.format(func_name),
                                    c.Fonts.table_default.format("function!"),
                                    c.Fonts.table_cog.format(percentage),
                                    c.Fonts.table_elapsed_time.format(f"{elapsed_time:.6f}")
                                )
            
                results = h.result_filter(results) if only_non_valids else results
                
                if show_table and len(results) != 0:
                    cls.print_result_table(results, pattern)

    @classmethod
    def print_result_table(cls, results, pattern: str=""):

        table = Table(show_header=True, header_style="bold blue", box=box.HEAVY)
        table.add_column("#", style="dim", width=h.max_digit_len(results), justify="center")
        table.add_column(f"Variables {pattern}", min_width=15)
        table.add_column("Expected", min_width=15)
        table.add_column("Output", min_width=15)
        table.add_column("Check", min_width=5, justify="center")

        for result in results:
            row, variables, expected, res, check = result
            row, variables, expected, res = h.convert_table_valid(row, variables, expected, res)
            passed_check = '✅' if check else '❌'
            table.add_row(
                            row,
                            variables,
                            expected,
                            res,
                            passed_check
                        )

        cls.console.print(table)
        
    @classmethod
    def print_passed_funcs(cls, result_data: dict={}, case_amount=0):
        passed_func = []
        for file_section in result_data.values():
            for data in file_section:
                if h.check_passed(data['result']):
                    passed_func.append(data)
        if passed_func:
            cls.console.print(c.Fonts.passed_success.format("Passed Function(s):"))
            cls.console.print(c.Fonts.passed_info.format(case_amount))
            for index, func in enumerate(passed_func):
                prefix = c.Fonts.passed_prefix
                prefix = c.Fonts.passed_lead_prefix if index==0 else prefix
                cls.console.print(c.Fonts.passed_row.format(prefix, func["name"], f"{func['elapsed']:5f}"))
        else:
            cls.console.print(c.Fonts.passed_error.format("No Function(s) has passed the test(s)."))

    @classmethod
    def print_json_data(cls, data):
        raw_json = json.dumps(data, indent=4)

        colorful_data = highlight(
            raw_json,
            lexer=JsonLexer(),
            formatter=Terminal256Formatter(),
        )

        print("\n".join([f"{index+1} "+row for index, row in enumerate(colorful_data.split("\n")[:-1])]))

    @classmethod
    def print_archive(cls, data):

        table = Table(show_header=True, header_style="bold blue", title_justify="left", box=box.HORIZONTALS)
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("Archive Name", min_width=20)
        table.add_column("Archive File Name (.txt)", min_width=15)

        archives = data["Create"]["archive-items"]
        for index, arc in enumerate(archives.items(), 1):
            arc_name, arc_val = arc
            table.add_row(str(index), arc_name, arc_val)

        cls.console.print(table)

    @classmethod
    def return_empty_help_table(cls, title, color=c.Colors.white):
        table = Table(show_header=True, header_style=f"bold {color}", title=c.Fonts.table_title.format(title), title_justify="left", box=box.HORIZONTALS)
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("Argument", min_width=10)
        table.add_column("Description", min_width=35)
        table.add_column("Default", min_width=7, justify="center")

        return table

    @classmethod
    def print_generated_variables(cls, variable_list):
        
        if not variable_list:
            cls.console.print(c.Fonts.passed_error.format("NO VARIABLE GENERATED"))
            return
        
        table = Table(show_header=True, title_style=f"bold {c.Colors.orange}", title="Generated Variables", header_style=f"bold {c.Colors.yellow}", box=box.HEAVY, min_width=20)
        table.add_column("#", style="dim")
        for i in variable_list[0]:
            table.add_column(str(i.__class__.__name__), justify="center")
        for index, var in enumerate(variable_list, 1):
            table.add_row(str(index), *[str(i) for i in var])
        cls.console.print(table)

    @classmethod
    def print_generated_archive(cls, archive_result=[]):
        table = Table(show_header=False, title_style=f"bold {c.Colors.magenta}", title="Archive Result", box=box.HEAVY, min_width=15)
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("Test Case", min_width=15, justify="center")

        for i, val in enumerate(archive_result, 1):
            table.add_row(str(i), val)

        cls.console.print(table)

    @classmethod
    def print_pattern_help(cls):
        
        # Number Rich Table
        number_table = cls.return_empty_help_table("NUMBER (num)", color=c.Colors.yellow)

        # Parameters
        number_table.add_row("1", "s (Start)", "If there is interval 's' help to declare start point", "5")
        number_table.add_row("2", "e (End)", "If there is interval 'e' help to declare end point", "10")
        number_table.add_row("3", "length", "If defined value is related to digit, this argument help to declare digit count", "5")
        number_table.add_row("4", "inval (Interval)", "Helps to change value as interval", "False")
        number_table.add_row("5", "dig (Digit)", "Helps to change value as digit", "False")
        number_table.add_row("-", c.Fonts.row_example_text, "num(s:2,e:6,inval:True)", "-")
        number_table.add_row("-", c.Fonts.row_example_text, "num(length:12,dig:True)", "-")

        # String Rich Table
        string_table = cls.return_empty_help_table("STRING (str)", color=c.Colors.red)

        string_table.add_row("1", "s (Start)", "If random args exists, start length of result string", "5")
        string_table.add_row("2", "e (End)", "If random args exists, end length of result string", "10")
        string_table.add_row("3", "length", "If random args not exists, declare length of random string", "5")
        string_table.add_row("4", "random", "Helps to declare if generated string will be integer or not", "False")
        string_table.add_row("-", c.Fonts.row_example_text, "str(s:3,e:5,random:True)", "-")
        string_table.add_row("-", c.Fonts.row_example_text, "str(length:7,random:False)", "-")

        # Boolean Rich Table
        boolean_table = cls.return_empty_help_table("BOOLEAN (bool)", color=c.Colors.blue2)

        boolean_table.add_row("1", "number", "Instead of generating value as True or False, generates as 0 and 1 s", "False")
        boolean_table.add_row("-", c.Fonts.row_example_text, "bool()", "-")
        boolean_table.add_row("-", c.Fonts.row_example_text, "bool(number:True)", "-")

        # Double Rich Table
        double_table = cls.return_empty_help_table("DOUBLE (dou)", color=c.Colors.magenta)
        
        double_table.add_row("1", "s (Start)", "'s' help to declare start point", "5.0")
        double_table.add_row("2", "e (End)", "'s' help to declare end point", "25.0")
        double_table.add_row("3", "rnd (Round)", "If 'rnd' arg declared function round value as 'rnd' digit after dot", "None")
        double_table.add_row("-", c.Fonts.row_example_text, "dou(s:7.34,e:64.2)", "-")
        double_table.add_row("-", c.Fonts.row_example_text, "dou(s:23.5,e:74.1,rnd:2)", "-")

        # List Rich Table
        list_table = cls.return_empty_help_table("LIST (list)", color=c.Colors.cyan)

        list_table.add_row("1", "s (Start)", "If order args exists, 's' helps to declare start point", "1")
        list_table.add_row("2", "e (End)", "If order args exists, 'e' helps to declare start point", "5")
        list_table.add_row("3", "order", "Helps to change list function status as ordered number list", "False")
        list_table.add_row("4", "times", "Declare 'times' amount element generated as given pattern in args", "5")
        list_table.add_row("5", "value_type", "Declaring type of first paranthesis parameters' function type", "None")
        list_table.add_row("6", "args (Arguments)", "With the help of first paranthesis, pattern could be declared for inner values too", "{}")
        list_table.add_row("-", c.Fonts.row_example_text, "list((s:3,e:8,random:True)(times:4,value_type:'str'))", "-")
        list_table.add_row("-", c.Fonts.row_example_text, "list((inval:True)(times:4,value_type:'num',order:True))", "-")

        # Dict Rich Table
        dict_table = cls.return_empty_help_table("DICT (dict)", color=c.Colors.green)

        dict_table.add_row("1", "times", "Declare 'times' amount element generated as gicen pattern in args", "5")
        dict_table.add_row("2", "key_type", "Declare to generate key argument type", "None")
        dict_table.add_row("3", "value_type", "Declare to generate value argument type", "None")
        dict_table.add_row("4", "key_args", "", "{}")
        dict_table.add_row("5", "value_args", "", "{}")
        dict_table.add_row("-", c.Fonts.row_example_text, "", "-")

        tables = [
            number_table,
            string_table,
            boolean_table,
            double_table,
            list_table,
            dict_table
            ]

        for table in tables:
            cls.console.print(table)
            print()

        cls.console.print(c.Fonts.table_title.format("RULES and EXCEPTIONS"))
        cls.console.print(c.Fonts.splitter_definition.format(f"Function Splitter defined as      {m_c.Vars.IO_CASE_SPLIT}"))
        cls.console.print(c.Fonts.splitter_definition.format(f"Variable Splitter defined as      {m_c.Vars.VARS_SPLIT}"))
        cls.console.print(c.Fonts.splitter_definition.format("Test Cases Splitter defined as    {}".format(m_c.Vars.TEST_SPLIT.replace("\n","\\n"))))
        cls.console.print(c.Fonts.splitter_definition.format(f"Main directory splitter define as {m_c.Vars.MAIN_DIR_SPLIT}"))
        cls.console.print(c.Fonts.splitter_definition.format("Recursive not working in pattern"))