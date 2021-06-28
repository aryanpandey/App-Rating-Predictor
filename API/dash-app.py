import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import dash
from flask import Flask

server = Flask(__name__)
app=dash.Dash(__name__,external_stylesheets = [dbc.themes.UNITED], suppress_callback_exceptions=True, server=server)

data = pd.read_csv('../Data/play_store_data.csv')

size_agg = data[data['size']>0].groupby(['genre', 'analysis_split']).agg({'size':'median'}).reset_index()

### Generating the graphs again
style_fig = go.Figure(data = [
            go.Bar(
                name='Apps with Rating < 3.7',
                x = size_agg[size_agg['analysis_split']==0]['genre'],
                y = size_agg[size_agg['analysis_split']==0]['size']
                ),
            go.Bar(
                name='Apps with Rating >= 3.7',
                x = size_agg[size_agg['analysis_split']==1]['genre'],
                y = size_agg[size_agg['analysis_split']==1]['size'] 
                )
    ])

genre_score_fig = px.box(data, x='genre', y='score', color='analysis_split')

price_fig = px.box(data[(data['price']<4500) & (data['free']==0)],
             x='genre', y='price', color='analysis_split')

review_agg = data.groupby(['genre', 'analysis_split']).agg({'reviews':'median'}).reset_index()
review_fig = go.Figure(data=[
    go.Bar(
    name = 'Apps with Rating < 3.7',
    x = review_agg[(review_agg['analysis_split'] == 0)&(review_agg['reviews']<5000)]['genre'],
    y = review_agg[(review_agg['analysis_split'] == 0)&(review_agg['reviews']<5000)]['reviews']
   ),
    go.Bar(
    name = 'Apps with Rating >=3.7',
    x = review_agg[(review_agg['analysis_split'] == 1)&(review_agg['reviews']<5000)]['genre'],
    y = review_agg[(review_agg['analysis_split'] == 1)&(review_agg['reviews']<5000)]['reviews']
   )
])

year_agg = data.groupby(['genre', 'analysis_split']).agg({'Years_from_release':'median'}).reset_index()

year_fig = go.Figure(data=[
    go.Bar(
    name = 'Apps with Rating < 3.7',
    x = year_agg[(year_agg['analysis_split'] == 0)]['genre'],
    y = year_agg[(year_agg['analysis_split'] == 0)]['Years_from_release']
   ),
    go.Bar(
    name = 'Apps with Rating >=3.7',
    x = year_agg[(year_agg['analysis_split'] == 1)]['genre'],
    y = year_agg[(year_agg['analysis_split'] == 1)]['Years_from_release']
   )
])

price_agg = data.groupby(['genre', 'analysis_split']).agg({'product_price':'median'}).reset_index()

IAPprice_fig = go.Figure(data=[
    go.Bar(
    name = 'Apps with Rating < 3.7',
    x = price_agg[(price_agg['analysis_split'] == 0)]['genre'],
    y = price_agg[(price_agg['analysis_split'] == 0)]['product_price']
   ),
    go.Bar(
    name = 'Apps with Rating >=3.7',
    x = price_agg[(price_agg['analysis_split'] == 1)]['genre'],
    y = price_agg[(price_agg['analysis_split'] == 1)]['product_price']
   )
])

col_list = {'Size vs Genre':style_fig, 'Score vs Genre':genre_score_fig,
            'Price vs Genre':price_fig, 'Reviews vs Genre': review_fig,
            'Years from Release vs Genre': year_fig, 
            'In App Product Price': IAPprice_fig}

## Designing the body of the app
body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H2("Welcome to the App Rating Predictor Website"),html.Br(),
                     html.Br(),html.Br(),
                     html.P("Use the menu on the top right corner to navigate through the page"),html.Br(),
                     html.P("You can view a few graphs in the Visualisation tab along with some of my insights from that graph"),html.Br(),
                     html.P("Or you can test out the model to predict the rating your app would get!!"),html.Br()
                   ],
               ), 
                ],style = {
            'textAlign': 'center',
            'color': '#7fDBFF',
            'backgroundColor':'#111111'}
            )
       ],style = {
            'backgroundColor':'#111111'
        })

layout_page_1 = html.Div(
        children = [
    html.H1(children = 'Visualisation Centre',
        style = {
            'textAlign': 'center',
            'color': '#7fDBFF',
            'backgroundColor':'#111111'}),
    html.P("Use the dropdown given below to change the graph displayed"),
    html.P("You'll be shown the graph along with a slight description of the graph as well as a few insights from it"),
    html.Div([
        html.Br(),
        dcc.Dropdown(
            id = 'plot_value',
            options = [{'label':i, 'value':i} for i in col_list.keys()],
            value = 'Size vs Genre'
            )
        ],style = {
            'color': '#7fDBFF',
            'backgroundColor':'#111111'
        }),
    dcc.Graph(id='indicator-graphic')
    ],style = {
            'textAlign': 'center',
            'color': '#7fDBFF',
            'backgroundColor':'#111111'
        })

layout_page_2 = html.Div(
        children = [
    html.H1(children = "Get your App's Rating now!!",
        style = {
            'textAlign': 'center',
            'color': '#7fDBFF',
            'backgroundColor':'#111111'}),
        html.Br(),
    html.H4(children = "Enter the following details about your app and click on the 'Get Rating' button",
        style = {
            'textAlign': 'center',
            'color':'#7fDBFF',
            'backgroundColor':'#111111'}
        ),
    html.Br(),
    dcc.Input(id="date", type="text", placeholder="Date of Release (DD/MM/YYYY)",
              style = {'marginLeft':'150px'}),
    dcc.Input(id="android", type="text", placeholder="Required Android Version",
              style = {'marginLeft':'200px'}),
    dcc.Input(id="ads", type="text", placeholder="App Contains Ads? (Y/N)",
              style = {'marginLeft':'200px'}),
    dcc.Input(id="currency", type="text", placeholder="The currency you deal in?",
              style = {'marginLeft':'200px'}),
    html.Br(),
    html.Br(),
    dcc.Input(id="devel", type="text", placeholder="Developing Company",
              style = {'marginLeft':'150px'}),
    dcc.Input(id="genre", type="text", placeholder="Genre of the App",
              style = {'marginLeft':'200px'}),
    dcc.Input(id="offersIAP", type="text", placeholder="Do you have In-App Purchases?(Y/N)",
              style = {'marginLeft':'200px', 'width':'14%'}),
    dcc.Input(id="price", type="number", placeholder="Price of the App",
              style = {'marginLeft':'192px'}),
    html.Br(),
    html.Br(),    
    dcc.Input(id="size", type="text", placeholder="Estimated Size of the App",
              style = {'marginLeft':'150px'}),
    dcc.Input(id="product_price", type="text", placeholder="Average Price of the In-App-Purchase Product",
              style = {'marginLeft':'200px', 'width':'18%'}),
    dcc.Input(id="min_age", type="text", placeholder="Minimum Age Required for Usage",
              style = {'marginLeft':'115px', 'width':'13.5%'}),
    dcc.Input(id="title", type="text", placeholder="App Name",
              style = {'marginLeft':'200px'}),
    html.Br(),
    html.Br(),
    dcc.Input(id="years_from_release", type="number", placeholder="After how many years from the App's Release do you want it's rating?",
              style = {'marginLeft':'150px', 'width':'27.5%'})
    ])

@app.callback(
    Output(component_id='indicator-graphic', component_property='figure'),
    Input(component_id='plot_value', component_property='value'))
def update_graph(graph_type):
    dff = col_list[graph_type]

    return dff

navbar = dbc.NavbarSimple(
           children=[
              dbc.DropdownMenu(
                 nav=True,
                 in_navbar=True,
                 label="Menu",
                 children=[
                    dbc.DropdownMenuItem("Visualisations",href="/insight"),
                    dbc.DropdownMenuItem("Get your App Rating!!",href="/model"),
                    
                          ],
                      ),
                    ],
          brand="Home",
          brand_href="/",
          sticky="top",)

page = html.Div(id = 'page-content')
url_bar = dcc.Location(id = 'url', refresh = False)

app.layout=html.Div([url_bar,navbar,page])

@app.callback([Output('page-content', 'children')],
              [Input('url', 'pathname')])
def display_page(pathname):
    #print(pathname)
    global cam
    if pathname == "/insight":
        return [layout_page_1]
    elif pathname == "/model":
        return [layout_page_2]
    else:
        return [body]

if __name__ == '__main__':
    app.run_server(debug = True)
