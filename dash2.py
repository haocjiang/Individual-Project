import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

all_datas = pd.read_table('./games.txt',sep='\t',encoding='gbk')
all_datas = all_datas.dropna(subset=["genre"])
all_types = list()
for item in all_datas.drop_duplicates(subset=['genre'], keep='first', inplace=False)['genre']:
    item_dict = {
        'label': item,
        'value': item
    }
    all_types.append(item_dict)

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

app.layout = html.Div([
    html.H1('Game Dashboard Analyse!', style={'textAlign': 'center'}),
    html.Br(),
    html.Div(
        [html.Div(["Type: ", dcc.Dropdown(options=all_types,
                                        id='type',
                                        value='Action'),
                  ],
                 style={'width': '33%', 'display': 'inline-block'}
                 ),
        html.Div(["Attribute: ", dcc.Dropdown(options=[{'label':'positive critics', 'value':'positive_critics'},
                                                       {'label':'neutral critics', 'value':'neutral_critics'},
                                                       {'label':'negative critics', 'value':'negative_critics'},
                                                       {'label':'positive users', 'value':'positive_users'},
                                                       {'label':'neutral users', 'value':'neutral_users'},
                                                       {'label':'negative users', 'value':'negative_users'},
                                                       {'label':'metascore', 'value':'metascore'},
                                                       {'label':'user score', 'value':'user_score'}],
                                        id='attribute',
                                        value='user_score'),
                  ],
                 style={'width': '33%', 'display': 'inline-block'}),
        html.Div(["Year: ", dcc.Dropdown(options=[{'label':'{}'.format(year), 'value':'{}'.format(year)} for year in range(2011,2020)],
                                          id='year',
                                          value='2011'),
                   ],
                  style={'width': '33%', 'display': 'inline-block'}
                  ),
         ]),
    html.Div(id='dash_table')
])


@app.callback(
    Output(component_id='dash_table', component_property='children'),
    [Input(component_id='type', component_property='value'),
     Input(component_id='attribute', component_property='value'),
     Input(component_id='year', component_property='value')]
)
def update_output_div(type, attribute, year):
    new_datas = all_datas[all_datas['genre']==type]
    new_datas = new_datas[new_datas['release_date'].str.contains('-'+year[-2:]+'$', na=True)]
    new_datas[attribute].astype('float')
    new_datas = new_datas.sort_values(by=attribute, ascending=False).head(15)
    return generate_table(new_datas)
    # return 'hello'

if __name__ == '__main__':
    app.run_server(debug=True)
