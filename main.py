from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

set_website_title("Crochet Calculator")
set_site_information(
    author="Megha Iyengar",
    description="Performs calculations related to crochet.",
    sources="Thanks to the Drafter docs.",
    planning=["Megha Iyengar - CS1 Final Project_design.pdf", "Megha Iyengar - CS1 Final Project_planning.pdf"],
    links=["https://miyengar-bot.github.io/crochet-calculator/"]
)
hide_debug_information()
set_website_framed(False)

set_website_style("daub")

@dataclass
class Yarn:
    cost_per_skein:float
    yards_per_skein:int
    weight:int

@dataclass
class Project:
    project_name:str
    hook_size:float
    yarn:Yarn

@dataclass
class State:
    projects:list[Project]
    current_page:str
    #results of the current calculator's calculations
    calculator_results:dict
    latest_result:float

def get_project(state:State, saved_project_name:str) -> Project:
    for project in state.projects:
        if project.project_name == saved_project_name:
            return project

# calculation functions:

def total_skeins(project:Project, total_yards:int) -> int:
    yarn = project.yarn
    return total_yards // yarn.yards_per_skein

def project_cost(project:Project, total_yards:int) -> float:
    yarn = project.yarn
    return total_skeins(project, total_yards) * yarn.cost_per_skein

def project_price(project:Project, crochet_time:int, total_yards:int) -> float:
    # base pricing
    yarn = project.yarn
    cost = project_cost(project, total_yards)
    hourly = crochet_time * 10
    return (cost * 3 + hourly) / 2

# route functions:

@route
def index(state:State) -> Page:
    state.current_page = 'Home'
    state.calculator_results = {}
    return Page(State(state.projects, state.current_page, state.calculator_results, state.latest_result),
                [change_text_decoration(change_color(change_text_align(Header("Crochet Calculator", 1), 'center'), '#38522f'), 'underline wavy'),
                Header('Select a calculator:', 2),
                 SelectBox("calculator", ['Gauge Calculator', 'Yarn Calculator', 'Money Calculator', 'Stitch Counter']),
                "\n",
                Button("Select", "select_calculator"),
                '\n\n',
                Div(Header("Add a Project!", 2),
                 Text('Project Name:'), TextBox('project_name'),
                 Text('Hook Size:'), TextBox('hook_size'),
                 '\n', '\n',
                 Header('Yarn:', 4),
                 Text('Cost Per Skein:'), TextBox('cost_per_skein'),
                 Text('Yards Per Skein:'), TextBox('yards_per_skein'),
                 Text('Weight:'), TextBox('weight'),
                Button("Add", "add_project")),
                '\n',
                Link("Show Projects", "show_projects")  
            ])

# project list modification functions:

@route
def add_project(state:State, project_name:str, hook_size:float, weight:int, cost_per_skein:float, yards_per_skein:int, calculator:str) -> Page:
    project = Project(project_name, hook_size, Yarn(weight, cost_per_skein, yards_per_skein))
    #if len(state.projects) < 3:
    state.projects.append(project)
    return index(state)
        
@route
def clear_projects(state:State) -> Page:
    state.projects = []
    return show_projects(state)

@route
def show_projects(state:State) -> Page:
    if len(state.projects) == 0:
        return Page(state, ['No saved projects', '\n', float_right(Link('Home', 'index'))])
    project_info = [change_color(Header('Projects', 1), '#e39d05'),
                    float_right(Button('Clear Projects', 'clear_projects'))
                    ]
    for index, project in enumerate(state.projects):
        name = project.project_name
        hook_size = str(project.hook_size)
        yarn_weight = str(project.yarn.weight)
        yarn_skein_cost = str(project.yarn.cost_per_skein)
        yarn_skein_yards = str(project.yarn.yards_per_skein)
        
        project_info.append(Header("Project: " + str(index + 1), 2))
        
        project_text = ['Name: ' + name,
                        '\n' + 'Hook Size: ' + hook_size,
                        '\n' + 'Yarn:',
                        '\n' + 'Weight: ' + yarn_weight,
                        '\n' + 'Cost Per Skein: ' + yarn_skein_cost,
                        '\n' + 'Yards Per Skein: ' + yarn_skein_yards,
                        '\n'
                        ]
        
        for item in project_text:
            project_info.append(item)
    project_info.append('\n')
    project_info.append(float_right(Link('Home', 'index')))
    return Page(state, project_info) 

# calculator functions:

@route 
def select_calculator(state:State, calculator:str) -> Page:
    state.current_page = calculator
    if calculator == 'Yarn Calculator':
        return yarn_calculator(state)
    elif calculator == 'Money Calculator':
        return money_calculator(state)
    elif calculator == 'Gauge Calculator':
        return gauge_calculator(state)
    elif calculator == 'Stitch Counter':
        return stitch_counter(state)
    
@route
def calculate_gague(state:State, stitches_length:float, stitch_count:int, rows_length:float,
                    row_count:int, desired_stitches_length:float, desired_rows_length:float) -> Page:
   
    state.calculator_results['swatch_stitches'] = stitch_count
    state.calculator_results['swatch_rows'] = row_count
    state.calculator_results['stitches_per_row_needed'] = round(stitch_count * desired_stitches_length / stitches_length)
    state.calculator_results['total_rows_needed'] = round(row_count * desired_rows_length / rows_length)
    total_stitches_needed = state.calculator_results['stitches_per_row_needed'] * state.calculator_results['total_rows_needed']
    state.calculator_results['total_stitches_needed'] = total_stitches_needed
    
    state.calculator_results['total_stitches_needed']
    
    return gauge_calculator(state)

@route
def gauge_calculator(state:State) -> Page:
    state.current_page = 'Gague Calculator'
                       
    if not state.calculator_results:
        state.calculator_results['stitches_per_row_needed'] = 0
        state.calculator_results['total_rows_needed'] = 0
        state.calculator_results['total_stitches_needed'] = 0
    
    return Page(state,
                [change_color(Header('Gague Calculator'), '#c25100'),
                 '\n',
                 Header('Swatch Measurements', 2),
                 '\n',
                 'Total length of stitches: ',
                 TextBox('stitches_length'),
                 'Stitch count: ',
                 TextBox('stitch_count'),
                 '\n',
                 'Total length of rows: ',
                 TextBox('rows_length'),
                 'Row count: ',
                 TextBox('row_count'),
                 '\n' + '\n',
                 Header('Desired Project Measurements', 2),
                 '\n',
                 'Total length of stitches: ',
                 TextBox('desired_stitches_length'),
                 '\n',
                 'Total length of rows: ',
                 TextBox('desired_rows_length'),
                 '\n',
                 Button('Calculate', 'calculate_gague'),
                 '\n',
                 'Total stitches needed per row: ' + str(state.calculator_results['stitches_per_row_needed']),
                 'Total rows needed: ' + str(state.calculator_results['total_rows_needed']),
                 'Total stitches needed: ' + str(state.calculator_results['total_stitches_needed']),
                 '\n',
                 Link('Calculate Yarn Needed', 'yarn_calculator'),
                 float_right(Link('Home', 'index'))
                 
                ])

@route
def calculate_yardage(state:State, swatch_mass:float, project:str) -> Page:
    saved_project = get_project(state, project)
    
    total_swatch_stitches = state.calculator_results['swatch_stitches'] * state.calculator_results['swatch_rows']  
    total_mass = (swatch_mass / total_swatch_stitches) * state.calculator_results['total_stitches_needed']
    total_yards = total_mass * saved_project.yarn.yards_per_skein / saved_project.yarn.weight
    
    state.calculator_results['total_yards'] = total_yards
    return yarn_calculator(state)

@route
def yarn_calculator(state:State) -> Page:
    state.current_page = 'Yarn Calculator'
    
    if not state.calculator_results:
        return Page(state, ['No swatch data. Please use the Gague Calculator first.',
                            '\n',
                            float_left(Link('Gague Calculator', 'gauge_calculator')),
                            float_right(Link('Home', 'index'))
                            ])
    
    saved_projects = []
    for project in state.projects:
        saved_projects.append(project.project_name)
    
    if 'total_yards' not in state.calculator_results:
        state.calculator_results['total_yards'] = 0
    
    return Page(state,
                [change_color(Header('Yarn Calculator'), '#c25100'),
                 Header('Select a project:', 3),
                 SelectBox("project", saved_projects),
                 '\n' + '\n' + 'Swatch Mass: ',
                TextBox('swatch_mass'),
                 '\n',
                Button('Calculate', 'calculate_yardage'),
                'Total yarn needed: ' + str(state.calculator_results['total_yards']),
                float_right(Link('Home', 'index'))
            ])

def clear_money_results(state:State) -> dict:
    state.calculator_results['total_skeins'] = 0
    state.calculator_results['project_cost'] = 0
    state.calculator_results['project_price'] = 0

@route
def calculate_money(state:State, project:str, crochet_time:int, total_yards:int) -> Page:
    saved_project = get_project(state, project)
    clear_money_results(state)
    state.calculator_results['total_skeins'] = (total_skeins(saved_project, total_yards))
    state.calculator_results['project_cost'] = (project_cost(saved_project, total_yards))
    state.calculator_results['project_price'] = (project_price(saved_project, crochet_time, total_yards))
    return money_calculator(state)

@route
def money_calculator(state:State) -> Page:
    state.current_page = 'Money Calculator'
    
    saved_projects = []
    for project in state.projects:
        saved_projects.append(project.project_name)
        
    if not state.calculator_results:
        clear_money_results(state)
        
    return_list = [change_color(Header('Money Calculator'), '#c25100'),
                     Header('Select a project:', 3),
                     SelectBox("project", saved_projects),
                     '\n' + '\n',
                     Header('Total yards: ', 4),
                     TextBox('total_yards'),
                    '\n' + 'Total Skeins = ' + str(state.calculator_results['total_skeins']),
                    '\n',
                    'Project Cost = ' + str(state.calculator_results['project_cost']),
                    '\n' + '\n',
                    Header('Crochet time: ', 4),
                    TextBox('crochet_time'),
                    '\n',
                    'Project Price = ' + str(state.calculator_results['project_price']),
                    '\n',
                    Button('Calculate', 'calculate_money'),
                    float_right(Link('Home', 'index'))
                    ]
            
    return Page(state, return_list)
                 
@route
def update_stitch_count(state:State, operation:str) -> Page:

    if operation == 'add_stitch':
        state.calculator_results['stitch'] += 1
    elif operation == 'subtract_stitch':
        if state.calculator_results['stitch'] > 0:
            state.calculator_results['stitch'] -= 1
    elif operation == 'add_stitch_5':
        state.calculator_results['stitch'] += 5
    elif operation == 'subtract_stitch_5':
        if state.calculator_results['stitch'] > 0:
            state.calculator_results['stitch'] -= 5
    elif operation == 'add_row':
        state.calculator_results['row'] += 1
    elif operation == 'subtract_row':
        if state.calculator_results['row'] > 0:
            state.calculator_results['row'] -= 1
        
    return stitch_counter(state)

@route
def stitch_counter(state:State) -> Page:
    state.current_page = 'Stitch Counter'
    
    if not state.calculator_results:
        state.calculator_results['stitch'] = 0
        state.calculator_results['row'] = 0
    
    return Page(state,
                [change_color(Header('Stitch Counter'), '#c25100'),
                 Header('Stitch Count: ' + str(state.calculator_results['stitch']), 2),
                 '\n',
                 Button('+1', 'update_stitch_count', [Argument("operation", "add_stitch")]),
                 Button('-1', 'update_stitch_count', [Argument("operation", "subtract_stitch")]),
                 Button('+5', 'update_stitch_count', [Argument("operation", "add_stitch_5")]),
                 Button('-5', 'update_stitch_count', [Argument("operation", "subtract_stitch_5")]),
                 '\n' + '\n',
                 Header('Row Count: ' + str(state.calculator_results['row']), 2),
                 '\n',
                 Button('+1', 'update_stitch_count', [Argument("operation", "add_row")]),
                 Button('-1', 'update_stitch_count', [Argument("operation", "subtract_row")]),
                 '\n',
                 float_right(Link('Home', 'index'))
        ])


start_server(State([], '', {}, 0.0))
