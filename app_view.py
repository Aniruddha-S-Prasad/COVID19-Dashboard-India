import json
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


def layout(github_img_url, linkedin_img_url):
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
                        html.H4(className='display-4 text-center', children='COVID-19 Dashboard')
                    ]),
                    html.Div(className='w-100', children=[]),
                    html.Div(className='col-lg-4', children=[
                        html.P(className='font-weight-normal text-center', children='Select a state'),
                        dbc.Select(
                            id='state',
                            className='shadow px-4 mb-1 bg-white rounded',
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
                    html.Div(className='card shadow px-4 mb-3 bg-white rounded', children=[
                        html.H3(className='card-title text-center pt-3', children='Total Cases'),
                        dcc.Graph(id='Total-Cases', className='graph', config={'displayModeBar': False})
                    ]),
                    html.Div(className='w-100', children=[]),
                    html.Div(className='card shadow px-4 mb-3 bg-white rounded', children=[
                        html.H3(className='card-title text-center pt-3', children='Active and Recovered Cases'),
                        dcc.Graph(id='Active-Cases', className='graph', config={'displayModeBar': False})
                    ])
                ]),
                html.Div(className='col-lg-4', children=[
                    html.Div(className='card shadow px-4 mb-1 bg-white rounded', children=[
                        html.H3(className='card-title text-center pt-3', children='Recovery Rate of Active Cases'),
                        html.P(className='card-text pl-3', children=['Probability of recovery from infection (Includes deceased cases)']),
                        dcc.Graph(id='Gamma', className='graph', config={'displayModeBar': False})
                    ]),
                    html.Div(className='w-100', children=[]),
                    html.Div(className='card shadow px-4 mb-1 bg-white rounded', children=[
                        html.H3(className='card-title text-center pt-3', children='Transmission Rate of Active Cases'),
                        html.P(className='card-text pl-3', children=['Probability of transmission of infection from an active case to a person in the general population']),
                        dcc.Graph(id='Beta', className='graph', config={'displayModeBar': False})
                    ])
                ]),
                html.Div(className='col-lg-4', children=[
                    html.Div(className='card shadow px-4 mb-1 bg-white rounded', children=[
                        html.H3(className='card-title text-center pt-3', children='Reproductive Number'),
                        html.P(className='card-text pl-3', children=['Number of additional infections caused by an infected person before recovery']),
                        dcc.Graph(id='R-0', className='graph', config={'displayModeBar': False})
                    ]),
                    html.Div(className='w-100', children=[]),
                    html.Div(className='card shadow px-4 mb-1 bg-white rounded', children=[
                        html.Div(className='card-text pl-1 py-3 ', children=[
                            html.Div(className=' align-items-center', children=[
                                html.Div(className='d-flex w-100 justify-content-between', children=[
                                    html.H5(className='mb-1', children='Data Sources'),
                                    html.Small(id='update-string',children='Default'),
                                ]),
                                html.P(className='mb-1 text-justify', children=[
                                    'All data presented in this dashboard is obtained from the ',
                                    html.A(href='https://www.covid19india.org/', target='_blank',children=['COVID-19 India']),
                                    ' project, using their ',
                                    html.A(href='https://api.covid19india.org/', target='_blank', children='API')
                                ]),
                            ]),
                            html.Hr(className='mb-1'),
                            html.Div(className='align-items-center pt-2', children=[
                                html.H5(className='mb-1', children='References'),
                                html.P(className='mb-1 text-justify', children=
                                    ['''The analysis provided in this dashboard follows the Susceptible, 
                                    Infected and Recovered model given by Yi-Cheng Chen et al. in  their paper ''',
                                    html.A(
                                        href='http://gibbs1.ee.nthu.edu.tw/A_TIME_DEPENDENT_SIR_MODEL_FOR_COVID_19.PDF',
                                        children='"A Time-dependent SIR model for COVID-19 with Undetectable Infected Persons".'
                                    )]
                                )
                            ]),
                            html.Hr(className='mb-1'),
                            html.Div(className='container pt-2', children=[
                                html.Div(className='row justify-content-center align-items-center', children=[
                                    html.Div(className='col', children=[
                                        html.A(className='btn btn-dark align-items-center', target='_blank',
                                            href='https://github.com/Aniruddha-S-Prasad/COVID19-Tracker/tree/web-development',
                                            children=[
                                                html.Img(className='icons', src=github_img_url),
                                                ' Contribute on Github'
                                            ]),
                                    ]),
                                    html.Div(className='col', children=[
                                        html.A(className='btn btn-light align-items-center', target='_blank',
                                            href='https://www.linkedin.com/in/aniruddha-sathyadharma-prasad/',
                                            children=[
                                                html.Img(className='icons', src=linkedin_img_url),
                                                '  Connect on Linkedin'
                                            ])
                                    ])
                                ])
                            ])
                        ]),
                        
                    ])
                ]),
                # html.Div(className='col-lg-1', children=[])
            ])
        ])
    ])

    return lyt

if __name__ == "__main__":
    raise EnvironmentError('Cannot run file')
