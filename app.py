import plotly.graph_objects as go
from plotly.offline import plot
import time
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

from config import CONFIGS

output_path = CONFIGS['output_path']

df_full = pd.read_csv(
    f'{output_path}/gold_price.csv',
    parse_dates=['timestamp'],
    float_precision='high'
)

# start plotting
products = df_full['product_std'].unique()

fig_price = go.Figure()
fig_price_diff = go.Figure()
fig_sell_premium = go.Figure()

for product in products:
    subset = df_full.loc[df_full['product_std'] == product]
    fig_price.add_traces(go.Scatter(
        x=subset['timestamp'], y=subset['sell_gr'], name=product, mode='lines'
    ))
    fig_price_diff.add_traces(go.Scatter(
        x=subset['timestamp'], y=subset['sell_gr'], name=product, mode='lines'
    ))
    fig_sell_premium.add_traces(go.Scatter(
        x=subset['timestamp'], y=subset['sell_gr'], name=product, mode='lines'
    ))

fig_price.update_layout(title='Price (BGN) per 1 gr pure gold')
fig_price_diff.update_layout(title='Price difference sell-buy (%) per 1 gr pure gold')
fig_sell_premium.update_layout(title='Seller premium (%) per 1 gr pure gold')

# create dash structure
app = dash.Dash(
    name='Gold Price',
    #external_stylesheets=[dbc.themes.BOOTSTRAP],
    #external_stylesheets=['./assets/bootstrap_adjusted.css'],
)
app.title = 'Gold Price'

content = (
    html.Div([
        html.H4('Gold Price', style={'padding-left':'10px'}),
        html.Br(), html.Br(),   
        html.Div(children=[
            dcc.Graph(figure=fig_price),
            html.Br(),
            dcc.Graph(figure=fig_price_diff),
            html.Br(),
            dcc.Graph(figure=fig_sell_premium),
            html.Br()
        ]),
        html.Br()
    ])
)

footer = html.Div(
    [
        html.Small("Designed by "),
        html.Small(html.A("Svilen Stefanov", href="https://www.linkedin.com/in/svilen-stefanov/", target="_blank")),
        html.Br(),
        html.Small(html.A("Source code", href="https://github.com/svilens/gold-price/", target="_blank")),
    ], style={'font-style':'italic', 'padding-left':'10px', 'textAlign':'left'}
)

app.layout = html.Div([
    html.H1(children='Gold Price', style={'padding-left':'5px'}),
    html.Br(),
    content,
    footer
])

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
