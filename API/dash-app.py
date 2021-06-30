import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import dash
from flask import Flask
import pickle

server = Flask(__name__)
app=dash.Dash(__name__,external_stylesheets = [dbc.themes.UNITED], suppress_callback_exceptions=True, server=server)

data = pd.read_csv('../Data/play_store_data.csv')

size_agg = data[data['size']>0].groupby(['genre', 'analysis_split']).agg({'size':'median'}).reset_index()

### Load models and encoders
les = {'currency': '../Model_Data/le_currency.pkl',
       'developer': '../Model_Data/le_developer.pkl',
       'genre': '../Model_Data/le_genre.pkl'}

models = {'model_0': '../Model_Data/model_0.pkl',
          'model_1': '../Model_Data/model_1.pkl',
          'model_2': '../Model_Data/model_2.pkl',
          'model_3': '../Model_Data/model_3.pkl',
          'model_4': '../Model_Data/model_4.pkl'}

for le in les.keys():
    les[le] = pickle.load(open(les[le], 'rb'))

for model in models.keys():
    models[model] = pickle.load(open(models[model], 'rb')) 

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

col_list = {'Size vs Genre':style_fig,
            'Price vs Genre':price_fig, 'Reviews vs Genre': review_fig,
            'Years from Release vs Genre': year_fig, 
            'In App Product Price vs Genre': IAPprice_fig}

desc_list = {'Size vs Genre': '''This is a simple Bar Chart which shows the Median size (in MB) of all apps in a genre,
                                 for each basket(Those with Rating < 3.7 and those with Rating >= 3.7).''',      
            'Price vs Genre':'''This is a Box Plot which shows the distribution of the prices of apps in a genre for each 
                                basket of apps(Those with Rating < 3.7 and those with Rating >= 3.7)''', 
            'Reviews vs Genre':'''This is a simple Bar Chart which shows the Median number of reviews of all apps in a genre,
                                 for each basket(Those with Rating < 3.7 and those with Rating >= 3.7)''',
            'Years from Release vs Genre':'''This is a simple Bar Chart which shows the Median Years from the time of release of all apps in a genre,
                                 for each basket(Those with Rating < 3.7 and those with Rating >= 3.7)''', 
            'In App Product Price vs Genre':'''This is a simple Bar Chart which shows the Median In-App Product Price of all apps in a genre,
                                 for each basket(Those with Rating < 3.7 and those with Rating >= 3.7)'''}

insight_list = {'Size vs Genre':'''Have added this graph here mainly for people to get an idea of how big an app they could keep
                                 if they haven't yet started the building phase''',
            'Price vs Genre':'''
                            Apps which have charged a higher price for education have received a higher rating (Maybe because of a thinking that expensive education is better?).
                            Apps in the personalization category have received a better rating if they had a lesser price.
                            Tools apps have a higher rating if they're more expensive''', 
            'Reviews vs Genre': '''In general it can be seen that the apps with a lower rating have lesser number of reviews given
                            from which we can reasonably say that the user base of apps with a lesser rating is significantly lesser.
                            Some of the reasons for apps like Social media apps getting a significantly higher number of reviews 
                            could be comments which offer criticism towards the app''',
            'Years from Release vs Genre': '''
                            For Action based apps, recent releases are given a higher rating compared to those from an older age, showing that apps in this genre can get outdated really quick if you don't bring out new updates.
                            Same can be said for communication, where apps which were released almost 5 years ago see a not so good rating on the app store. People love new updates in communication.
                            In genres like medical apps, consumers like to go ahead with something that they can trust and has been established. This is shown by older apps getting a higher rating in comparison to the more recent apps.
                            With News, the population likes staying up to date and since a majority of the people have shifted to E-News between 3-4 years ago, any apps published during that time have been riding that wave till date''', 
            'In App Product Price vs Genre': '''
                            Categories like Business, Dating, Finance, Health and Fitness, News and Magazines and Travel are ones were you should keep a significantly lower price when compared to it's median value shown.
                            If you want to monetize the app and still maintain a high rating for it, categories like Action, Adventure, Card, Communication, House and Home, Shopping, Simulation, Social, Strategy and Trivia can offer you good returns'''}

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
    html.P("You'll be shown the graph along with a slight description of what the graph is about as well as a few of my insights from it"),
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
    html.Br(),
    html.P(id = 'graph_desc'),
    dcc.Graph(id='indicator-graphic'),
    html.H4('Insights'),
    html.P(id='insights')
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
    dcc.Input(id="size", type="text", placeholder="Estimated Size of the App(in MB)",
              style = {'marginLeft':'150px'}),
    dcc.Input(id="product_price", type="text", placeholder="Average Price of the In-App-Purchase Product",
              style = {'marginLeft':'200px', 'width':'18%'}),
    dcc.Input(id="min_age", type="text", placeholder="Minimum Age Required for Usage(in Years)",
              style = {'marginLeft':'115px', 'width':'13.5%'}),
    dcc.Input(id="years_from_release", type="number", placeholder="After how many years from the App's Release do you want it's rating?",
              style = {'marginLeft':'50px', 'width':'27.5%'}),
    html.Br(),
    html.Br(),    
    html.Button("Get Rating", id = 'get_rating', n_clicks=0, style={'marginLeft':'950px'}),
    html.Br(),
    html.Br(),
    html.P(id='model_output', style = {
            'textAlign': 'center',
            'color':'#7fDBFF',
            'backgroundColor':'#111111'})
    ])

@app.callback(
    Output(component_id='model_output', component_property='children'),
    Input(component_id='date', component_property='value'),
    Input(component_id='android', component_property='value'),
    Input(component_id='ads', component_property='value'),
    Input(component_id='currency', component_property='value'),
    Input(component_id='devel', component_property='value'),
    Input(component_id='genre', component_property='value'),
    Input(component_id='offersIAP', component_property='value'),
    Input(component_id='price', component_property='value'),
    Input(component_id='size', component_property='value'),
    Input(component_id='product_price', component_property='value'),
    Input(component_id='min_age', component_property='value'),
    Input(component_id='years_from_release', component_property='value'),
    Input(component_id='get_rating', component_property='n_clicks'))
def get_rating(date, android, ads, currency, devel, genre, offersIAP, price,
                size, product_price, min_age, years_from_release, get_rating):
    if get_rating>0:
        try:
            currency = les['currency'].transform(currency)
        except:
            currency = -1
        try:
            devel = les['developer'].transform(devel)
        except:
            devel = -1
        try:
            genre = les['genre'].transform(genre)
        except:
            genre = -1

        try:
            day = int(date.split('/')[0])
            month = int(date.split('/')[1])
            year = int(date.split('/')[2])
        except:
            day = -1
            month = -1
            year = -1
        try:
            android = int(android.split('.')[0])
        except:
            android = -1
        
        if offersIAP.lower() == 'y':
            offersIAP = 1
        elif offersIAP.lower() == 'n':
            offersIAP = 0
        else:
            offersIAP = -1
        
        if ads.lower() == 'y':
            ads = 1
        elif ads.lower() == 'n':
            ads = 0
        else:
            ads = -1
        
        try:
            size = int(size)
        except:
            size = -1

        try:
            product_price = int(product_price)
        except:
            product_price = -1

        try:
            min_age = int(min_age)
        except:
            min_age = -1

        data = {'Day':[day],
                'Month':[month],
                'Year':[year],
                'androidVersion':[android],
                'containsAds':[ads],
                'currency':[currency],
                'developer':[devel],
                'genre':[genre],
                'offersIAP':[offersIAP],
                'price':[price],
                'size':[size],
                'Years_from_release':[years_from_release],
                'product_price':[product_price]}
            
        data = pd.DataFrame(data).T
        
        pred = np.argmax((models['model_0'].predict_proba(data) + 
                          models['model_1'].predict_proba(data) +
                          models['model_2'].predict_proba(data) + 
                          models['model_3'].predict_proba(data) +
                          models['model_4'].predict_proba(data)))

        score_dict = {0:'0-1.75',1:'1.75-3',2:'3-4',3:'4-4.5',4:'4.5-5'}

        return 'App Rating: ' + score_dict[pred]
 
@app.callback(
    Output(component_id='indicator-graphic', component_property='figure'),
    Output(component_id='graph_desc', component_property='children'),
    Output(component_id='insights', component_property='children'),
    Input(component_id='plot_value', component_property='value'))
def update_graph(graph_type):
    dff = col_list[graph_type]
    desc = desc_list[graph_type]

    insight = insight_list[graph_type]
    insights = []
    for i in insight.split('.'):
        insights.append(i)
        insights.append(html.Br())
        insights.append(html.Br())

    return [dff, desc, insights]

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
