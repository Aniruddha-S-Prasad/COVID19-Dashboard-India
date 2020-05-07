import json
import dash_core_components as dcc
import dash_html_components as html


def layout():
    with open('databases/state_codes.json') as state_codes:
        state_dict = json.load(state_codes)

    lyt = html.Div(children=[
        html.Div(id='init-viewport',className='large-display', children=[
            html.Div(className='container-fluid', children=[
                html.Div(className='row align-items-center justify-content-center', children=[
                    html.Div(className='col-8', children=[
                        html.H4(className='display-4 text-center', children='COVID-19 Dashboard')
                    ]),
                    html.Div(className='w-100', children=[]),
                    html.Div(className='col-5', children=[
                        dcc.Dropdown(id="state", options=[{"label":state_name,"value":state_code} 
                            for state_code, state_name in state_dict.items()], 
                            value=None),
                    html.Div(className='w-100', children=[])
                    ])
                ])
            ])
        ]),
        html.P(children=['     ']),
        html.Div(className='container-fluid', children=[
            html.Div(className='row justify-content-center align-items-center', children=[
                # html.Div(className='col-lg-1', children=[]),
                html.Div(className='col-lg-4', children=[
                    html.Div(className='card shadow px-4 mb-3 bg-white rounded', children=[
                        html.H4(className='card-title text-center pt-3', children='Total Cases'),
                        dcc.Graph(id='Total-Cases')
                    ]),
                    html.Div(className='w-100', children=[]),
                    html.Div(className='card shadow px-4 mb-3 bg-white rounded', children=[
                        html.H4(className='card-title text-center pt-3', children='Active and Recovered Cases'),
                        dcc.Graph(id='Active-Cases')
                    ])
                ]),
                html.Div(className='col-lg-4', children=[
                    html.Div(className='card shadow px-4 mb-1 bg-white rounded', children=[
                        html.H4(className='card-title text-center pt-3', children='Recovery Rate of Active Cases'),
                        html.P(className='card-text pl-5', children=['Probability of recovery from infection (Includes deceased cases)']),
                        dcc.Graph(id='Gamma')
                    ]),
                    html.Div(className='w-100', children=[]),
                    html.Div(className='card shadow px-4 mb-1 bg-white rounded', children=[
                        html.H4(className='card-title text-center pt-3', children='Transmission Rate of Active Cases '),
                        html.P(className='card-text pl-5', children=['Probability of transmission of infection from an active case to a person in the general population']),
                        dcc.Graph(id='Beta')
                    ])
                ]),
                html.Div(className='col-lg-4', children=[
                    html.Div(className='card shadow px-4 mb-1 bg-white rounded', children=[
                        html.H4(className='card-title text-center pt-3', children='Reproductive Number'),
                        html.P(className='card-text pl-5', children=['Number of additional infections caused by an infected person before recovery']),
                        dcc.Graph(id='R-0')
                    ])
                ]),
                # html.Div(className='col-lg-1', children=[])
            ])
        ])
    ])

    return lyt

if __name__ == "__main__":
    raise EnvironmentError('Cannot run file')
