from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Crochet Calculator")
set_website_framed(False)

set_website_style("almond")

@dataclass
class Yarn:
    weight: int
    cost_per_skein: float
    yards_per_skein: int

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
    calculator_results:list[float]
    latest_result:float

def get_project(state:State, saved_project_name:str) -> Project:
    for project in state.projects:
        if project.project_name == saved_project_name:
            return project

# calculation functions:

def total_skeins(project:Project, total_yards:int) -> int:
    yarn = project.yarn
    return total_yards // yarn.yards_per_skein

def project_cost(project:Project, total_yards: int) -> float:
    yarn = project.yarn
    return total_skeins(yarn.yards_per_skein, total_yards) * cost_per_skein

def project_price(project: Project, crochet_time: int, total_yards: int) -> float:
    # base pricing
    yarn = project.yarn
    cost = project_cost(yarn.cost_per_skein, yarn.yards_per_skein, total_yards)
    hourly = crochet_time * 10
    return (cost * 3 + hourly) / 2


# route functions:

@route
def index(state:State) -> Page:
    state.current_page = 'Home'
    return Page(State(state.projects, state.current_page, state.calculator_results, state.latest_result),
                [(change_text_align(Header("Crochet Calculator", 1), 'center')),
                Header('Select a calculator:', 2),
                 SelectBox("calculator", ['Yarn Calculator', 'Money Calculator', 'Gauge Calculator', 'Stitch Counter']),
                "\n",
                Button("Select", "select_calculator"),
                '\n\n',
                Div(Header("Add a Project!", 2),
                 Text('Project Name:'), TextBox('project_name'),
                 Text('Hook Size:'), TextBox('hook_size'),
                 '\n', '\n',
                 Text('Yarn:'),
                 '\n',
                 Text('Weight:'), TextBox('weight'),
                 Text('Cost Per Skein:'), TextBox('cost_per_skein'),
                 Text('Yards Per Skein:'), TextBox('yards_per_skein'),
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
        return Page(state, ['No saved projects', '\n', change_text_align(Link('Home', 'index'), right)])
    project_info = [Header('Projects', 1),
                    Button('Clear Projects', 'clear_projects')
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
    project_info.append(change_text_align(Link('Home', 'index'), right))
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
def calculate_increase(state:State) -> Page:
   return yarn_calculator(state)

@route
def yarn_calculator(state:State) -> Page:
    state.current_page = 'Yarn Calculator'
    return Page(state,
                [Header('Yarn Calculator'),
                'Increase Count: ',
                 '\n',
                Button('Calculate', 'calculate_increase'), 
                change_text_align(Link('Home', 'index'), 'right')
            ])

@route
def calculate_money(state:State, project:str, crochet_time:int, total_yards:int) -> Page:
    saved_project = get_project(state, project)
    
    #need to add the results to the page
    state.calculator_results.append(total_skeins(saved_project, total_yards))
    #'Project Cost = ' + str(
    state.calculator_results.append(project_cost(project, total_yards))
    #'Project Price = ' + str
    state.calculator_results.append(project_price(project, crochet_time, total_yards))
    return money_calculator(state)

@route
def money_calculator(state:State) -> Page:
    state.current_page = 'Money Calculator'
    saved_projects = []
    for project in state.projects:
        saved_projects.append(project.project_name)
        
    return_list = [Header('Money Calculator'),
                 Header('Select a project:', 3),
                 SelectBox("project", saved_projects),
                 '\n' + 'Total yards: ',
                 TextBox('total_yards')
                   ]
                 
    if len(state.calculator_results) >= 1:   
     return_list.append('Total Skeins = ' + str(state.calculator_results[0]))
     return_list.append('Project Cost = ' + str(state.calculator_results[1]))
    
    return_list.append('\n' + 'Crochet time: ')
    return_list.append(TextBox('crochet_time'))
    return_list.append('\n')
    return_list.append(Button('Calculate', 'calculate_money')) 
    return_list.append('\n')
     
    if len(state.calculator_results) == 2:
     return_list.append('Project Price = ' + str(state.calculator_results[2]))
    
    
     change_text_align(Link('Home', 'index'), 'right')
    
    return Page(state, return_list)
                 
@route
def calculate_gague(state:State, stitch_count:int) -> Page:
    return gauge_calculator(state)

@route
def gauge_calculator(state:State) -> Page:
    state.current_page = 'Gague Calculator'
    return Page(state,
                [Header('Gague Calculator'),
                 TextBox('stitch_count'),
                change_text_align(Link('Home', 'index'), 'right')
            ])
@route
def add_stitch(state:State) -> Page:
    return stitch_counter(state)

@route
def stitch_counter(state:State) -> Page:
    state.current_page = 'Stitch Counter'
    return Page(state,
                [Header('Stitch Counter'),
                 Header('Stitch Count: ', 2),
                 '\n',
                 Button('+1', 'add_stitch'),
                 Button('-1', 'add_stitch'),
                 '\n',
                 Header('Row Count: ', 2),
                 '\n',
                 Button('+1', 'add_stitch'),
                 Button('-1', 'add_stitch'),
                 change_text_align(Link('Home', 'index'), 'right')
        ])


start_server(State([], '', [], 0.0))
