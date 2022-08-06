from dash import Dash, html, dcc, Input, Output, dash_table,callback
from dash.exceptions import PreventUpdate
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html,dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import json
app = Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.ZEPHYR])
df1 = pd.read_csv('https://github.com/Themaoyc/MDA/blob/main/Data/temperaturedata_predict.csv?raw=true')
df2 = pd.read_csv('https://github.com/Themaoyc/MDA/blob/main/Data/deaths_predict.csv?raw=true')
df2.drop(['ISO','CPI'], axis=1,inplace=True)
df2long = df2.melt(id_vars = ['Country', 'Year'],
                    value_vars = ['tmax','duration','GDP(million dollars)','Population','healthexp','Associated Drought',
                   'Associated Wildfire','Appeal or Declaration','Total Deaths'],
                    var_name = 'Indicator Name',
                    value_name = 'Value')
df3 = pd.read_csv('https://github.com/Themaoyc/MDA/blob/main/Data/Latitude%26Longitude.csv?raw=true')
df4 = pd.read_csv('https://github.com/Themaoyc/MDA/blob/main/Data/emdat%20heatwave.csv?raw=true')
df3 = df3.rename(columns={'Alpha-3 code':'ISO'})
df4 = df4[['ISO','Year']]
df5 = pd.merge(df4,df3,on=['ISO'],how='left')
df5 = df5[['Country','Year','Latitude (average)','Longitude (average)']]



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
    dcc.Tabs(id="tabs-inline", value='tab-1', parent_className='custom-tabs',className='custom-tabs-container',
             children=[
        dcc.Tab(label='Homepage', value='Homepage', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Predict Heatwaves', value='Predict Heatwaves', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Predict Deaths', value='Predict Deaths', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Tab 4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs-inline', 'value'))
def render_content(tab):
    if tab == 'Homepage':
        return html.Div([
            html.H1('MDA Project Heatwave',style={'textAlign': 'center'}),
            html.Div([
                dcc.Graph(id='World Heatwave'),

                dcc.Slider(
                    df5['Year'].min(),
                    df5['Year'].max(),
                    step=None,
                    id='year--slider1',
                    value=df5['Year'].max(),
                    marks={str(year): str(year) for year in df5['Year'].unique()},

                )], style={'width': '48%', 'textAlign': 'center', 'float': 'center', 'display': 'inline',
                           'margin-left': '-300px', 'margin-right': '-300px'})
        ])
    elif tab == 'Predict Heatwaves':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'Predict Deaths':
        return  html.Div([
    html.Div([
        html.H3('Predict deaths',style={'textAlign': 'center'}),
        html.H4('In this part, we try to use GDP, health expenditure, population, max temperature during the heatwave,'
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

    )],style={'width': '48%', 'textAlign': 'center','float': 'center', 'display': 'inline','margin-left':'-300px','margin-right':'-300px'})

])

    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
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
                    )

    fig1.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig1.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig1.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig1
@app.callback(
    Output('World Heatwave', 'figure'),
    Input('year--slider1', 'value'))
def update_graph(year_value1):
    df5f = df5[df5['Year'] == year_value1]

    fig2 = go.Figure(go.Scattermapbox(
                                      mode='markers',
                                      lon=df5f[2],
                                      lat=df5f[3],
                                      hovertext='Country',
                                      hoverinfo='text',
                                      marker_symbol='marker',
                                      marker_size=10
                                      ))

    fig2.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')


    return fig2

if __name__ == '__main__':
    app.run(debug=True, threaded=True)



#fig2 = px.scatter_mapbox(df5, lat="Latitude (average)", lon="Longitude (average)",     color="peak_hour", size="car_hours",
                  #color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)