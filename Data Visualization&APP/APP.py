from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app=Dash(__name__,suppress_callback_exceptions=True,external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)
df1 = pd.read_csv('https://github.com/Themaoyc/MDA/blob/main/Data/temperaturedata_predict.csv?raw=true')
df1long = df1.melt(id_vars=['Country', 'Year','Heatwave'],
                   value_vars=['January', 'February','March','April','May'],
                   var_name='Month',
                   value_name='tavg')
df2 = pd.read_csv('https://github.com/Themaoyc/MDA/blob/main/Data/deaths_predict.csv?raw=true')
df2new = df2.drop(['ISO', 'CPI'], axis=1)
df2long = df2new.melt(id_vars=['Country', 'Year'],
                   value_vars=['tmax', 'duration', 'GDP(million dollars)', 'Population', 'healthexp',
                               'Associated Drought',
                               'Associated Wildfire', 'Appeal or Declaration', 'Total Deaths'],
                   var_name='Indicator Name',
                   value_name='Value')
a3 = ['Logistic Regression','KNN','Decision Tree','Bagging','Random Forest','Gradient Boosting','Logistic Regression','KNN','Decision Tree','Bagging','Random Forest','Gradient Boosting']
b3 = [0.5,0.5286850021486893,0.6462183068328319,0.6368715083798884,0.5548990116029222,0.5905672539750751,0.9322916666666666,0.9192708333333334,0.8723958333333334,0.7552083333333334,0.9348958333333334,0.9348958333333334]
c3 = ['AUC','AUC','AUC','AUC','AUC','AUC','Accuracy','Accuracy','Accuracy','Accuracy','Accuracy','Accuracy']
df3 = pd.DataFrame({'Models':a3,'value':b3,'AUC/Accuracy':c3})
df4 = pd.read_csv('https://github.com/Themaoyc/MDA/blob/main/Data/emdat%20heatwave.csv?raw=true')
df4 = df4[['ISO','Year','Disaster Subtype']]
df5 = pd.DataFrame({'Months':['January','February','March','April','May','January','February','March','April','May'],
                  'Temperature':[3.515534,4.762336,8.013707,12.058991,16.281385,1.711976,2.580137,6.013315,10.489134,14.739301],
                 'Group':['None Heatwave','None Heatwave','None Heatwave','None Heatwave','None Heatwave','Heatwave','Heatwave','Heatwave','Heatwave','Heatwave']})
x1 = np.arange(30, 50,0.01)
y1 = np.exp(0.1059*x1+1.9218442)
df6 = pd.DataFrame({'Tmax':x1,'Predict Deaths':y1})
df7 = pd.read_csv('https://github.com/Themaoyc/MDA/blob/main/Data/topic.csv?raw=true')

app=Dash(__name__)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
    html.H1('MDA Project Heatwave', style={'textAlign': 'center'}),
    html.H3('Yicheng Mao R0865820', style={'textAlign': 'center'}),
    html.Div(
        [html.Div([
            html.Img(
                src='https://github.com/Themaoyc/MDA/blob/main/Data%20Visualization%26APP/assets/picture1.png?raw=true'),
        ])
        ], style={'textAlign': 'center'}),
    dcc.Tabs(id="tabs-inline", value='tab-1', parent_className='custom-tabs', className='custom-tabs-container',
             children=[
                 dcc.Tab(label='Homepage', value='Homepage', style=tab_style, selected_style=tab_selected_style),
                 dcc.Tab(label='Predict Heatwaves', value='Predict Heatwaves', style=tab_style,
                         selected_style=tab_selected_style),
                 dcc.Tab(label='Predict Deaths', value='Predict Deaths', style=tab_style,
                         selected_style=tab_selected_style),
                 dcc.Tab(label='Topic Modeling', value='Topic Modeling', style=tab_style,
                         selected_style=tab_selected_style),
             ], style=tabs_styles),
    html.Div(id='tabs-content'),

])


@app.callback(Output('tabs-content', 'children'),
              Input('tabs-inline', 'value'))
def render_content(tab):
    if tab == 'Homepage':
        return html.Div([
            html.H1('MDA Project Heatwave', style={'textAlign': 'center'}),
            html.H3('These years, public are paying more and more attention to heat waves as such '
                    'extreme meteorological may could lead to massive deaths . '
                    'In order to have a better knowledge on the damage due to heat waves, '
                    'our group decide to predict the heatwave and deaths caused by heatwaves.'),

            html.Div([
                dcc.Graph(id='World Heatwave',figure=px.choropleth(df4, locations="ISO",
                                                                   color="Disaster Subtype",  animation_frame="Year",
                                                                   )),

                ], style={'width': '60%', 'textAlign': 'center', 'float': 'center', 'display': 'inline',
                           'margin-left': '-300px', 'margin-right': '-300px'}),
            html.H6('Worldwide Heatwave Map', style={'textAlign': 'center'})
        ])
    elif tab == 'Predict Heatwaves':
        return html.Div([
            html.H1('Predict Heatwaves', style={'textAlign': 'center'}),
            html.H3('In this part, we try to use the monthly average temperature from January to February'
                    'to predict whether there will be a heatwave during the summer. '),
            html.Div([
                dcc.Graph(id='AVGt'),

                dcc.Slider(
                    df1long['Year'].min(),
                    df1long['Year'].max(),
                    step=None,
                    id='year--slider3',
                    value=df1long['Year'].max(),
                    marks={str(year): str(year) for year in df1long['Year'].unique()},

                )], style={'width': '48%', 'textAlign': 'center', 'float': 'center', 'display': 'inline',
                           'margin-left': '-300px', 'margin-right': '-300px'}),
            html.H3('We can see that the group with a heatwave in the future has a different trend line'),
            html.Div(
                [html.Div([
                dcc.Graph(id='Heatwavetemperaturem',figure=px.line(df5, x='Months', y='Temperature',color='Group')),
                    ])
                 ], style={'textAlign': 'center'}),
            html.H3('We choose the monthly average temperature and country as independent variables and '
                    'build different models to predict heatwave.'),

            html.Div(
                [html.Div([
                dcc.Graph(id='Heatwave models',figure=px.bar(df3, x='Models', y='value',color='AUC/Accuracy')),
                    ])
                 ], style={'textAlign': 'center'}),
            html.H3('Among all the models, Decision Tree model the one works best in terms of Accuracy and AUC')

        ])

    elif tab == 'Predict Deaths':
        return html.Div([
            html.Div([
                html.H1('Predict deaths', style={'textAlign': 'center'}),
                html.H3('World Heatwave Deaths Map',style={'textAlign': 'center'}),
                html.Div([
                    dcc.Graph(id='World Heatwave Deaths', figure=px.choropleth(df2, locations="ISO",
                                                                        color="Total Deaths",
                                                                        animation_frame="Year",
                                                                        )),

                ], style={'width': '60%', 'textAlign': 'center', 'float': 'center', 'display': 'inline',
                          'margin-left': '-300px', 'margin-right': '-300px'}),
                html.H3(
                    'In this part, we try to use GDP, health expenditure, population, max temperature during the heatwave,'
                    'duration of the heatwave,associated disaster, and the declaration in advance to predict the total deaths'
                    'of a heatwave. The correlations of these variables are shown as follows: '),
                html.Div([
                    html.H5('Xaxis'),
                    dcc.Dropdown(
                        df2long['Indicator Name'].unique(),
                        'tmax',
                        id='xaxis-column'
                    ),
                    dcc.RadioItems(
                        ['Linear', 'Log'],
                        'Linear',
                        id='xaxis-type',
                        inline=True
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),

                html.Div([
                    html.H5('Yaxis'),
                    dcc.Dropdown(
                        df2long['Indicator Name'].unique(),
                        'Total Deaths',
                        id='yaxis-column'
                    ),
                    dcc.RadioItems(
                        ['Linear', 'Log'],
                        'Linear',
                        id='yaxis-type',
                        inline=True
                    )
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
            ]),
            html.Div([
                dcc.Graph(id='Predict deaths1'),

                dcc.Slider(
                    df2long['Year'].min(),
                    df2long['Year'].max(),
                    step=None,
                    id='year--slider2',
                    value=df2long['Year'].max(),
                    marks={str(year): str(year) for year in df2long['Year'].unique()},

                )], style={'width': '48%', 'textAlign': 'center', 'float': 'center', 'display': 'inline',
                           'margin-left': '-300px', 'margin-right': '-300px'}),
            html.H3('The negative binomial model is applied to predict the total deaths to fix the overdispersion of poisson model.'
                    'We know this june a heatwave happened in Belgium, though the temperature data and deaths data are still not available. '
                    'Here we use our model to predict the deaths caused by this heatwave in Belgium.'),
            html.Div(
                [html.Div([
                    dcc.Graph(id='Heatwave deaths Belgium',
                              figure=px.line(df6,x='Tmax',y='Predict Deaths')),
                ])
                ], style={'textAlign': 'center'}),


        ])

    elif tab == 'Topic Modeling':
        return html.Div([
            html.H1('Topic Modeling', style={'textAlign': 'center'}),
            html.H3('In this part, we collected 1000 core comments from Reddit with the key word Heatwave.', style={'textAlign': 'center'}),
            html.H3('WordCloud', style={'textAlign': 'center'}),

            html.Div(
                [html.Div([
                    html.Img(
                        src='https://github.com/Themaoyc/MDA/blob/main/Data%20Visualization%26APP/assets/wordcloud.png?raw=true'),
                ])
                ], style={'textAlign': 'center'}),
            html.H3('LDA model is applied to determine cluster words.',
                    style={'textAlign': 'center'}),
            html.Div([
                dcc.Dropdown(
                    df7['topic'].unique(),
                    'Topic1',
                    id='Topic'
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='topic model'),
            html.H3('Top 10 Words for each Topic', style={'textAlign': 'center'}),
        ])


@app.callback(
    Output('Predict deaths1', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('year--slider2', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value2):
    df2longf = df2long[df2long['Year'] == year_value2]

    fig1 = px.scatter(x=df2longf[df2longf['Indicator Name'] == xaxis_column_name]['Value'],
                      y=df2longf[df2longf['Indicator Name'] == yaxis_column_name]['Value'],
                      hover_name=df2longf[df2longf['Indicator Name'] == yaxis_column_name]['Country'],
                      color=df2longf[df2longf['Indicator Name'] == yaxis_column_name]['Country'],
                      size=df2longf[df2longf['Indicator Name'] == yaxis_column_name]['Value']
                      )

    fig1.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig1.update_xaxes(title=xaxis_column_name,
                      type='linear' if xaxis_type == 'Linear' else 'log')

    fig1.update_yaxes(title=yaxis_column_name,
                      type='linear' if yaxis_type == 'Linear' else 'log')

    return fig1



@app.callback(
    Output('AVGt', 'figure'),
    Input('year--slider3', 'value'))
def update_graph(year_value3):
    df1longf = df1long[df1long['Year'] == year_value3]
    fig3 = px.scatter(df1longf, x="Month", y="tavg", color="Heatwave")

    def update_output_div(input_value):
        return f'Output: {input_value}'

    fig3.update_layout(margin={"r": 20, "t": 0, "l": 20, "b": 10})


    return fig3

@app.callback(
    Output('topic model', 'figure'),
    Input('Topic', 'value'))
def update_graph(topic):
    df7f = df7[df7['topic'] == topic]
    fig_topic = px.bar(df7f,
                       x='Word',
                       y='Weight',
                       color='Word',
                    )
    fig_topic.update_layout(showlegend=False)
    return fig_topic

if __name__ == '__main__':
    app.run(debug=True, threaded=True,dev_tools_ui=False,dev_tools_props_check=False)


