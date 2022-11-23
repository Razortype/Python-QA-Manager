## MAIN PATH IMPORTING
from pathlib import Path
import os

## MODULES IMPORTING
from generator.generator import RandomGenerator as RG
from manager.manager import DeployManager
from manager.manager import CreateManager
from manager.manager import TestManager
from display.display import Display as DP

## Clien Application -| Rich / Console / Typer application implementing
import typer

## Creates Required Objects (for the managing and demonstration purposes)
app = typer.Typer(help='Client-Based function quality and efficiency tester.')

## Manager objects' installation
MAIN_DIR = Path(os.getcwd()).parent.absolute()
random_generator = RG()
deploy_manager = DeployManager(MAIN_DIR)
create_manager = CreateManager(MAIN_DIR, random_generator)
test_manager = TestManager(MAIN_DIR)

@app.command()
def funcs(detail: bool = typer.Option(
                help='Detailed information of validated functions\' will be demonstrated too.',
                default=False
            )):
    """
    Scan and validate functions with respected to predetermined directories in 'data.json' file.\n
    with --detail property, more detailed information of validation functions will be demonstrated
    """
    test_manager.load_funcs()
    DP.print_funcs(test_manager.funcs, detailed=detail)

@app.command()
def data(change: bool = typer.Option(
                help="After demonstration of 'data.json' file, system will ask for change.",
                default=False
            )):
    """
    Pretty print 'data.json' file
    """
    DP.print_json_data(deploy_manager.get_data())
    if change:
        print(" -- UNDER CONTRUCTION -- ")
    

@app.command()
def create(show: bool = typer.Option(
                help="Documentation displayed as table for creating a valid pattern.",
                default=False
            ),
            pattern: str = typer.Option(
                help='''Declaring pattern for creating arguments for function. Needed for creating a valid test scenarios.''',
                default=None
            ),
            func_name: str = typer.Option(
                help='''Declaring pre-written function for generated variables. Needed for creating a valid test scenarios.''',
                default=None
            ),
            amount: int =typer.Option(
                help='''Helps to declare n amount test scenarios.''',
                default=1
            ),
            save: bool = typer.Option(
                help="Manager will ask if created data should be saved in archive or not",
                default=False
            )
            ):
    """
    Creates test case senarious with given pattern and function.
    '--pattern' and '--func-name' are required for creating valid test cases
    use '--save' with other properties to save results
    """

    if show:
        DP.print_pattern_help()
        return
    
    test_manager.load_funcs()
    create_manager.deploy_pattern(pattern)
    
    if pattern and not func_name:
        # DP print executed variables
        for _ in range(amount):
            create_manager.evaluate_pattern()
            print(create_manager.generated_variables)
    
    if pattern and func_name:
        
        func_meta = test_manager.get_func_by_name(func_name)
        create_manager.deploy_process_func(func_meta)
        create_manager.process_func_results(amount)

        archive_result = create_manager.conver_to_archive()
        
        # DP print executed variables
        print("\n".join(archive_result))
        
        if save:
            deploy_manager.save_archive(archive_result)
            print("Archived Successfully")

@app.command()
def load(case_name: str = typer.Option(
                help="Load existing data to test assets/cases.txt",
                default=None
            ),
            show: bool = typer.Option(
                help="Shows table before assignment",
                default=False
            )
            ):
    """
    Loads existing case data to system.
    """
    if show:
        DP.print_archive(deploy_manager.get_data())
    else:
        deploy_manager.deploy_testcase(case_name)
    
@app.command()
def run(funcs: str = typer.Option(
                help='''Initially, functions can be indicated. If there is no function declared, all function will be tested. use comma between function names ("func1,func2")''',
                default="all##"
            ),
            table: bool = typer.Option(
                help='''Demonstrate result of test cases.''',
                default = True
            ),
            filter: bool = typer.Option(
                help='''Displays only filtered (WRONG) test case(s).''',
                default = False
            ),
            passed: bool = typer.Option(
                help='''Demonstrate litte section for passed function that ordered with elapsed time.''',
                default = False
            )
        ):
    """
    Runs preloaded test-case senarious with declared functions.\n
    If --no-table is used, there will be no table to demonstrate\n
    If --filter is used, filters the results\n
    If --passed is used, creates a passed table
    """
    deploy_manager.load_case()
    test_manager.load_funcs(funcs)
    test_manager.run_all(deploy_manager.input_lst, deploy_manager.output_lst)
    
    DP.print_results(test_manager.funcs, show_table=table, only_non_valids=filter, pattern=deploy_manager.get_pattern(string=True))
    if passed:
        DP.print_passed_funcs(test_manager.funcs,deploy_manager.get_case_amount())

if __name__ == "__main__":
    app()