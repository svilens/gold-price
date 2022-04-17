import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_dark"
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
products = sorted(df_full['product_std'].unique())

fig_price = go.Figure()
fig_price_diff = go.Figure()
fig_sell_premium = go.Figure()

for product in products:
    subset = df_full.loc[df_full['product_std'] == product]
    fig_price.add_traces(go.Scatter(
        x=subset['timestamp'], y=subset['sell_gr'], name=product, mode='lines',
        hovertemplate='<i>%{y:.2f}</i>, ' + '%{x}'
    ))
    fig_price_diff.add_traces(go.Scatter(
        x=subset['timestamp'], y=subset['price_diff_gr'], name=product, mode='lines',
        hovertemplate='<i>%{y:.2f}</i>, ' + '%{x}'
    ))
    fig_sell_premium.add_traces(go.Scatter(
        x=subset['timestamp'], y=subset['sell_gr_premium'], name=product, mode='lines',
        hovertemplate='<i>%{y:.2f}</i>, ' + '%{x}'
    ))

fig_price.update_layout(title='Price (BGN) per 1 gr pure gold')
fig_price_diff.update_layout(title='Price margin sell-buy (%) per 1 gr pure gold')
fig_sell_premium.update_layout(title='Seller premium (%) per 1 gr pure gold')

df_last = df_full.loc[df_full['timestamp'] == df_full['timestamp'].max()].copy()
df_last.iloc[:,2:]
df_last['loss_per_gr'] = df_last['sell_gr'] - df_last['buy_gr']
df_last['sell_gr_rank'] = df_last['sell_gr'].rank()
df_last['loss_per_gr_rank'] = df_last['loss_per_gr'].rank()
df_last['rank'] = (df_last['sell_gr'].rank() + df_last['loss_per_gr'].rank())/2

fig_rank_loss = go.Figure()
fig_rank_loss.add_traces(go.Bar(
    x=df_last.sort_values(by='loss_per_gr_rank')['product_std'],
    y=df_last.sort_values(by='loss_per_gr_rank')['loss_per_gr_rank']
))
fig_rank_loss.update_layout(title='RANK 2: Lowest loss per gr')

fig_rank_sell = go.Figure()
fig_rank_sell.add_traces(go.Bar(
    x=df_last.sort_values(by='sell_gr_rank')['product_std'],
    y=df_last.sort_values(by='sell_gr_rank')['sell_gr_rank']
))
fig_rank_sell.update_layout(title='RANK 1: Lowest sell price per gr')

fig_rank_avg = go.Figure()
fig_rank_avg.add_traces(go.Bar(
    x=df_last.sort_values(by='rank')['product_std'],
    y=df_last.sort_values(by='rank')['rank']
))
fig_rank_avg.update_layout(title='RANK - average')


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
            html.Br(),
            dcc.Graph(figure=fig_rank_sell),
            html.Br(),
            dcc.Graph(figure=fig_rank_loss),
            html.Br(),
            dcc.Graph(figure=fig_rank_avg),
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
