
class Colors:
    green = "green"
    blue = "#2196F3"
    orange = "#ff9800"
    red = "#f44336"
    gray = "#e7e7e7"

    magenta = "magenta"
    yellow = "yellow"
    cyan = "cyan"
    
    cyan2 = "#2E8BC0"
    gray2 = "#696969"
    blue2 = "blue"

    white = "#ffffff"

class Fonts:
    
    NONE = "[red bold][red bold]"

    row_example_text = f" ↳ [{Colors.orange}] EXAMPLE [/{Colors.orange}]"

    func_table_title = f"📁 [{Colors.magenta}]" + "{}" + f"[/{Colors.magenta}]"
    func_table_default = table_default= f"[italic {Colors.gray2}]" + "{}" + f"[/italic {Colors.gray2}]"
    func_table_error = f"  ❌ [{Colors.red} underline bold]" + "{}" + f"[/{Colors.red} underline bold]"
    func_table_name = f"[{Colors.yellow} bold]"+"{}" + f"[/{Colors.yellow} bold]"
    func_table_element = f"[{Colors.gray}]" + "{}" + f"[/{Colors.gray}]"
    func_table_index = f"[{Colors.green}]" + "{}" + f"[/{Colors.green}]"

    table_title = f"[bold {Colors.magenta}]" + "{}" + f"[/bold {Colors.magenta}]"
    table_default= f"[italic {Colors.gray}]" + "{}" + f"[/italic {Colors.gray}]"
    table_cog = f"⚙️ [{Colors.yellow}] "+"{}" + f"%[/{Colors.yellow}]"
    table_elapsed_time = f" [{Colors.cyan}]" + "{}" + f" second elapsed[/{Colors.cyan}] ⌛"
    table_processing = f"[{Colors.magenta} underline italic]" + "{}" + f"[/{Colors.magenta} underline italic]"

    passed_success = f"✅ [{Colors.green} underline bold]" + "{}" + f"[/{Colors.green} underline bold]"
    passed_error = f"❌ [{Colors.red} underline bold]" + "{}" + f"[/{Colors.red} underline bold]"
    passed_info = f" [{Colors.gray2} italic]#Total case amount: " + "{}" + f"[/{Colors.gray2} italic]"
    passed_row = "{}" + f"[{Colors.magenta}]" + "{}"+f"[/{Colors.magenta}] " + f"[{Colors.cyan2}](" + "{}" + f"s)[/{Colors.cyan2}]"
    passed_prefix = f" [{Colors.blue} bold]-> [/{Colors.blue} bold]"
    passed_lead_prefix = " 👑"+f" [{Colors.blue} bold]-> [/{Colors.blue} bold]"
    
    splitter_definition = f"  ➡ [{Colors.cyan2}]" + "{}" + f"[/{Colors.cyan2}]"