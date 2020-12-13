import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

all_datas = pd.read_table('./games.txt',sep='\t',encoding='gbk')
all_datas = all_datas.dropna(subset=["genre"])
all_types = list()
all_type_dict = {
    'label': 'All',
    'value': 'All'
}
all_types.append(all_type_dict)
for item in all_datas.drop_duplicates(subset=['genre'], keep='first', inplace=False)['genre']:
    item_dict = {
        'label': item,
        'value': item
    }
    all_types.append(item_dict)

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

app.layout = html.Div([
    html.H1('Game Dashboard Analysis!', style={'textAlign': 'center'}),
    html.Br(),
    html.Div(["Type: ", dcc.Dropdown(options=all_types,
                                    id='type',
                                    value='Action'),
              ],
             style={'width': '33%', 'display': 'inline-block'}
             ),
    html.Div(["Attribute: ", dcc.Dropdown(options=[{'label':'number', 'value':'number'},
                                                   {'label':'positive critics', 'value':'positive_critics'},
                                                   {'label':'neutral critics', 'value':'neutral_critics'},
                                                   {'label':'negative critics', 'value':'negative_critics'},
                                                   {'label':'positive users', 'value':'positive_users'},
                                                   {'label':'neutral users', 'value':'neutral_users'},
                                                   {'label':'negative users', 'value':'negative_users'},
                                                   {'label':'metascore', 'value':'metascore'},
                                                   {'label':'user score', 'value':'user_score'}],
                                    id='attribute',
                                    value='number'),
              ],
             style={'width': '33%', 'display': 'inline-block'}
             ),
    html.Div([dcc.Graph(id='rolls_fig')])
])


@app.callback(
    Output(component_id='rolls_fig', component_property='figure'),
    [Input(component_id='type', component_property='value'),
     Input(component_id='attribute', component_property='value')]
)
def update_output_div(type, attribute):
    years_list = [item for item in range(2011, 2020)]
    y_list = [item for item in range(11, 20)]
    if type != 'All':
        data_list = all_datas[all_datas['genre'].str.contains(type + '$', na=True)]
        df = pd.DataFrame({'year':years_list})
        results = list()
        for every_year in y_list:
            datas_year = data_list[data_list['release_date'].str.contains('-' + str(every_year) + '$', na=True)]
            if attribute == 'number':
                game_count = datas_year['release_date'].count()
            else:
                datas_year[attribute].astype('int')
                game_count = datas_year[attribute].sum()
            results.append(game_count)
        df[type] = results
        fig = px.bar(df, x='year', y=type, barmode="group")
        fig.update_layout(title="%s of %s games per year " % (attribute,type),
                          xaxis_title="Year",
                          yaxis_title=attribute)
    else:
        df = pd.DataFrame({'year': years_list})
        new_data = all_datas.drop_duplicates(subset=['genre'], keep='first', inplace=False)
        for game_type in new_data['genre']:
            data_list = all_datas[all_datas['genre'].str.contains(game_type + '$', na=True)]
            all_years_count = []
            for every_year in y_list:
                datas_year = data_list[data_list['release_date'].str.contains('-' + str(every_year) + '$', na=True)]
                if attribute == 'number':
                    game_count = datas_year['release_date'].count()
                else:
                    datas_year[attribute].astype('int')
                    game_count = datas_year[attribute].sum()
                all_years_count.append(game_count)
            df[game_type] = all_years_count
        fig = px.line(df, x="year", y=df.columns[1:])
        fig.update_layout(title="%s of %s games per year " % (attribute, type),
                          xaxis_title="Year",
                          yaxis_title=attribute,
                          legend_title="Type",
                          font=dict(
                              family="Courier New, monospace",
                              size=18,
                              color="RebeccaPurple")
                          )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
