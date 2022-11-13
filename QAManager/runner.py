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
def valids(detail: bool = typer.Option(
                help='Table will be demonstrate function with much more detailed and informative versions',
                default=False
            )):
    """
    Displays valid functions in fetched function directory.\n
    If --detail is not used, given information and detail will be restricted
    """
    test_manager.load_funcs()
    DP.print_funcs(test_manager.funcs, detailed=detail)

@app.command()
def data(change: bool = typer.Option(
                help="data.json file be demonstrated and ask for replacement.",
                default=False
            )):
    """
    Demonstrate current data object's varaibles and their values.
    """
    DP.print_json_data(deploy_manager.get_data())
    if change:
        print(" -- UNDER CONTRUCTION -- ")
    

@app.command()
def create(pattern: str = typer.Option(
                help='''Creating test-case with given VARIABLES. (ex:"<variable_type>('s':5,'e':10)")''',
                default=None
            ),
            func_name: str = typer.Option(
                help='''Creating test-case with given FUNCTION NAME. (ex:"<func_name>")''',
                default=None
            ),
            amount: int =typer.Option(
                help='''Creating "amount" test case''',
                default=1
            ),
            save: bool = typer.Option(
                help="Manager will ask if created data should be saved in archive or not",
                default=False
            ),
            show: bool = typer.Option(
                help="Variables and functions will be demonstrated for creating a pattern",
                default=False
            )
            ):
    """
    Creates test case senarious with given pattern.
    """

    if show:
        DP.print_pattern_help()
        return
    
    test_manager.load_funcs()
    create_manager.deploy_pattern(pattern)
    
    if pattern and not func_name:
        create_manager.evaluate_pattern()
        # DP print executed variables
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
                help='''Decleration of function names. If func_names empthy it returns all## keyword that makes all function running.''',
                default="all##"
            ),
            table: bool = typer.Option(
                help='''Displays table, default value is True''',
                default = True
            ),
            filter: bool = typer.Option(
                help='''Displays only filtered(wrong) test case''',
                default = False
            ),
            passed: bool = typer.Option(
                help='''Creates a little table for passed function and order by elapsed time''',
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