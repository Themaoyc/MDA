import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html,dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
df
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])

#这里还不清楚是不是上网用的 server = app.server


if __name__ == "__main__":
    app.run_server(debug=True)
