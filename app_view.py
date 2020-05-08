import json
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


def layout():
    with open('databases/state_codes.json') as state_codes:
        state_dict = json.load(state_codes)

    states_dropdown = []
    for state_code, state_name in state_dict.items():
        states_dropdown.append({"label":state_name,"value":state_code})

    lyt = html.Div(children=[
        html.Div(id='init-viewport', className='large-display', children=[
            html.Div(className='container-fluid', children=[
                html.Div(className='row align-items-center justify-content-center', children=[
                    html.Div(className='col-lg-8', children=[
                        html.H1(className='display-4 text-center', children='COVID-19 Dashboard')
                    ]),
                    html.Div(className='w-100', children=[]),
                    html.Div(className='col-lg-4', children=[
                        html.P(className='font-weight-normal text-center', children='Select a state'),
                        dbc.Select(
                            id='state',
                            options=states_dropdown,
                        ),
                    html.Div(className='w-100', children=[])
                    ])
                ])
            ])
        ]),
        html.Div(className='container-fluid', children=[
            html.Div(className='row justify-content-center align-items-center', children=[
                # html.Div(className='col-lg-1', children=[]),
                html.Div(className='col-lg-4', children=[
                    html.Div(className='card shadow px-4 mb-3 bg-white rounded', style={'max-width': '50rem'}, children=[
                        html.H4(className='card-title text-center pt-3', children='Total Cases'),
                        dcc.Graph(id='Total-Cases', className='graph', config={'displayModeBar': False})
                    ]),
                    html.Div(className='w-100', children=[]),
                    html.Div(className='card shadow px-4 mb-3 bg-white rounded', style={'max-width': '50rem'}, children=[
                        html.H4(className='card-title text-center pt-3', children='Active and Recovered Cases'),
                        dcc.Graph(id='Active-Cases', className='graph', config={'displayModeBar': False})
                    ])
                ]),
                html.Div(className='col-lg-4', children=[
                    html.Div(className='card shadow px-4 mb-1 bg-white rounded', style={'max-width': '50rem'}, children=[
                        html.H4(className='card-title text-center pt-3', children='Recovery Rate of Active Cases'),
                        html.P(className='card-text pl-5', children=['Probability of recovery from infection (Includes deceased cases)']),
                        dcc.Graph(id='Gamma', className='graph', config={'displayModeBar': False})
                    ]),
                    html.Div(className='w-100', children=[]),
                    html.Div(className='card shadow px-4 mb-1 bg-white rounded', style={'max-width': '50rem'}, children=[
                        html.H4(className='card-title text-center pt-3', children='Transmission Rate of Active Cases '),
                        html.P(className='card-text pl-5', children=['Probability of transmission of infection from an active case to a person in the general population']),
                        dcc.Graph(id='Beta', className='graph', config={'displayModeBar': False})
                    ])
                ]),
                html.Div(className='col-lg-4', children=[
                    html.Div(className='card shadow px-4 mb-1 bg-white rounded', style={'max-width': '50rem'}, children=[
                        html.H4(className='card-title text-center pt-3', children='Reproductive Number'),
                        html.P(className='card-text pl-5', children=['Number of additional infections caused by an infected person before recovery']),
                        dcc.Graph(id='R-0', className='graph', config={'displayModeBar': False})
                    ])
                ]),
                # html.Div(className='col-lg-1', children=[])
            ])
        ])
    ])

    return lyt

if __name__ == "__main__":
    raise EnvironmentError('Cannot run file')
