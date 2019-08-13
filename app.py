# -*- coding: utf-8 -*-
# Import libraries
import os

import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_daq as daq
import plotly.graph_objs as go

import imdb
ia = imdb.IMDb()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True
app.title = 'TV Series Ratings & Analysis'

# Master container
app.layout = dbc.Container(
    className="parent-container",
    children=[
        dcc.Tabs(id="main-tabs", children=[
            # Tab 1
            dcc.Tab(label='Series Ratings', children=[
                dbc.Row([
                    dbc.Col(
                        children = [
                            dcc.Input(
                                id='search-input',
                                className='search-dropdown',
                                placeholder="Search for a series...",
                                autoComplete='off'
                            ),
                            html.Div(
                                dcc.RadioItems(
                                    options=[],
                                    id="series-radio",
                                    className='results_radio'
                                ),
                                className='results_div',
                                id='results-div',
                            ),
                        ]
                    )],
                    className='searchRow'
                ),
                dbc.Row([
                    dbc.Col([
                        # Show details widget parent div
                        html.Div(
                            id="series-widget",
                            className="series_widget",
                            )
                        ]),
                        dbc.Col([
                            # Season slider
                            html.Div(
                                className='season-slider-container',
                                children = [
                                    dcc.RangeSlider(
                                        id='season-slider',
                                        disabled= True,
                                        marks={1: '1', 2: '2'},
                                        max=2,
                                        value=[1,2],
                                        count=1,
                                        min=1,
                                        step=1,
                                        included = True,
                                        vertical = False,
                                        allowCross = False,
                                    ),
                                ]
                            ),
                            html.H4(id='slider-text'),
                            html.Div(
                                className='season-slider-autoscale-container',
                                id='season-slider-autoscale-container',
                                children = [
                                    html.H5("Autoscale Y-axis: "),
                                    daq.ToggleSwitch(
                                        id='my-toggle-switch',
                                        value=True,
                                        color='#CF676F',
                                    ),
                                ]
                            )
                        ],
                        style={
                            'paddingLeft': '10px'
                        }),
                    ],
                    className='widgetRow',
                    id='widget-row'
                ),
                dbc.Row([
                    # Initial
                    dbc.Col(
                        children = [
                            html.H2("Welcome!"),
                            html.P("This application lets you search for a series and check out the IMDb rating of each episode on a graph."),
                            html.P("You can then also look up an episode and see how the votes were distributed."),
                            html.P("Finally, add a second series to see how they compare to one another."),
                            html.H4("Search for a show to get started")
                        ]
                    )
                ],
                className='graphRow',
                id='graph1-row-empty',
                style={'display': 'block'}
                ),
                dbc.Row([
                    #Graph
                    dbc.Col(
                        children = [
                        dcc.Graph(
                            id='ratings_graph',
                        ),
                    ])
                ],
                className='graphRow',
                id='graph1-row',
                style={'visibility': 'hidden'}
                ),
            ]),
            # Tab 2
            dcc.Tab(label='Episode Rating Breakdown', id='tab-2', disabled=True, children=[
                dbc.Row(
                    className="rating_breakdown_selection",
                    children = [
                        dbc.Col(
                            children = [
                                html.Div(
                                    children = [
                                        html.Div(
                                            id="breakdown-series-widget",
                                            className="series_widget"
                                        ),
                                        dbc.Row([
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id='breakdown-season-dropdown',
                                                    searchable=False,
                                                    placeholder="Select a season"
                                                )
                                            ),
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id='breakdown-episode-dropdown',
                                                    searchable=False,
                                                    placeholder="Select an episode"
                                                )
                                            )
                                        ],
                                        style={'marginTop': '10px'})
                                    ]
                                ),
                            ]
                        ),
                        dbc.Col(
                            children = [
                                html.Div(
                                    id = 'breakdown-details',
                                    className = 'breakdown-episode-details',
                                    children = [
                                        html.H3(id="breakdown-episode-name"),
                                        html.Div([
                                            html.Div(
                                                className = "score-circle",
                                                children = [
                                                    html.H3(id="breakdown-episode-score")
                                                ]
                                            ),
                                            html.H5("IMDb Score")
                                        ], className='score-circle-container'),
                                        html.Div([
                                            html.Div(
                                                className = "score-circle",
                                                children = [
                                                    html.H3(id="breakdown-episode-mean")
                                                ]
                                            ),
                                            html.H5("Mean")
                                        ], className='score-circle-container'),
                                        html.Div([
                                            html.Div(
                                                className = "score-circle",
                                                children = [
                                                    html.H3(id="breakdown-episode-median")
                                                ]
                                            ),
                                            html.H5("Median")
                                        ], className='score-circle-container'),
                                    ]
                                )
                            ],
                        )
                    ]
                ),
                dbc.Row(
                    className="rating_breakdown_graph",
                    id='breakdown-row-empty',
                    style={'display': 'block'},
                    children = [
                        html.H4("Select a season and episode to view the rating breakdown")
                    ]
                ),
                dbc.Row(
                    className="rating_breakdown_graph",
                    id='breakdown-row',
                    style={'visibility': 'hidden'},
                    children = [
                        dcc.Graph(
                            id='breakdown-graph',
                        ),
                    ]
                )
            ]),
            # Tab 3
            dcc.Tab(label='Compare Series', id='tab-3', disabled=True, children=[
                dbc.Row([
                    dbc.Col(
                        children = [
                            dcc.Input(
                                id='search-input2',
                                className='search-dropdown',
                                placeholder="Search for a series to compare it to...",
                                autoComplete='off'
                            ),
                            html.Div(
                                dcc.RadioItems(
                                    options=[],
                                    id="series2-radio",
                                    className='results_radio'
                                ),
                                className='results_div',
                                id='results2-div',
                            ),
                        ]
                    )],
                    className='searchRow'
                ),
                dbc.Row([
                    dbc.Col([
                        # Show details widget parent div
                        html.Div(
                            id="series-widget-compare",
                            className="series_widget",
                        ),
                        html.Div(
                            id="series2-widget",
                            className="series2_widget",
                        )
                    ]),
                        dbc.Col([
                            # Season slider
                            html.Div(
                                className='season-slider-container',
                                children = [
                                    dcc.RangeSlider(
                                        id='season2-slider',
                                        disabled= True,
                                        marks={1: '1', 2: '2'},
                                        max=2,
                                        value=[1,2],
                                        count=1,
                                        min=1,
                                        step=1,
                                        included = True,
                                        vertical = False,
                                        allowCross = False,
                                    ),
                                ]
                            ),
                            html.H4(id='slider2-text'),
                            html.Div(
                                className='season-slider-autoscale-container',
                                id='season-slider-autoscale-container2',
                                children = [
                                    html.H5("Autoscale Y-axis: "),
                                    daq.ToggleSwitch(
                                        id='my-toggle-switch2',
                                        value=True,
                                        color='#CF676F',
                                    ),
                                ]
                            )
                        ],
                        style={
                            'paddingLeft': '10px'
                        }),
                    ],
                    className='widgetRow',
                    id='widget-row2'
                ),
                dbc.Row([
                    # Initial
                    dbc.Col(
                        children = [
                        html.H4("Search for a second series to compare it to")
                    ])
                ],
                className='graphRow',
                id='graph2-row-empty',
                style={'display': 'block'}
                ),
                dbc.Row([
                    #Graph
                    dbc.Col(
                        children = [
                        dcc.Graph(
                            id='ratings2_graph',
                        ),
                    ])
                ],
                className='graphRow',
                id='graph2-row',
                style={'visibility': 'hidden'}
                ),
            ]),
        ])
    ]
)

#Searching for series 1 and getting results
@app.callback(
    Output(component_id='series-radio', component_property='options'),
    [Input(component_id='search-input', component_property='value')])
def search_series(input):
    if input==None:
        return []
    if input!=None:
        result = ia.search_movie(input)
        series = []
        for i in result:
            if i['kind']=='tv series':
                series.append(i)
        return [{'label': i['title'], 'value': i.movieID} for i in series]

#Searching for series 2 and getting results
@app.callback(
    Output(component_id='series2-radio', component_property='options'),
    [Input(component_id='search-input2', component_property='value')])
def search_series2(input):
    if input==None:
        return []
    if input!=None:
        result = ia.search_movie(input)
        series = []
        for i in result:
            if i['kind']=='tv series':
                series.append(i)
        return [{'label': i['title'], 'value': i.movieID} for i in series]

#Selecting series 1
@app.callback(
    [Output(component_id='series-widget', component_property='children'),
     Output(component_id='series-widget-compare', component_property='children'),
     Output(component_id='season-slider', component_property='marks'),
     Output(component_id='season-slider', component_property='max'),
     Output(component_id='season-slider', component_property='value'),
     Output(component_id='season-slider', component_property='disabled'),
     Output(component_id='breakdown-series-widget', component_property='children'),
     Output(component_id='tab-2', component_property='disabled'),
     Output(component_id='tab-3', component_property='disabled'),
     Output(component_id='graph1-row', component_property='style'),
     Output(component_id='graph1-row-empty', component_property='style'),
     Output(component_id='widget-row', component_property='style')],
    [Input(component_id='series-radio', component_property='value')])
def select_show(input):
    if input == None:
        return [], [], {1: '1', 2: '2'}, 2, [1,2], True, [], True, True, {'visibility': 'hidden'}, {'display': 'block'}, {'display': 'none'}
    while input != None:
        show_widget = []
        series_details = ia.get_movie(input)
        series_name = series_details['title']
        show_widget.append(
            html.Div([
                html.Div([
                    html.Img(
                        src = series_details['cover url']
                    )
                ]),
                html.Div(
                    style = {
                        'width': '100%',
                    },
                    children = [
                        # Show title div
                        html.Div(
                            className='series-widget-title',
                            children = [
                                html.H2(series_name, style = {'margin': '0'}),
                            ]
                        ),
                        html.Div(
                            className='series-widget-details',
                            children = [
                                html.H5(str(series_details['seasons']) + " seasons "),
                                html.H5(series_details['series years']),
                                html.H5("IMDb Score: " + str(series_details['rating'])),
                                html.H5(id='selected_result')
                            ]
                        )
                    ]
                ) 
            ])
        )
        return show_widget, show_widget, {i: 'Season {}'.format(i) for i in range(1, series_details['seasons'])}, series_details['seasons'],[1, series_details['seasons']], False, show_widget, False, False, {'visibility': 'visible'}, {'display': 'none'}, {}

#Selecting series 2
@app.callback(
    [Output(component_id='series2-widget', component_property='children'),
     Output(component_id='season2-slider', component_property='marks'),
     Output(component_id='season2-slider', component_property='max'),
     Output(component_id='season2-slider', component_property='value'),
     Output(component_id='season2-slider', component_property='disabled'),
     Output(component_id='graph2-row', component_property='style'),
     Output(component_id='graph2-row-empty', component_property='style'),
     Output(component_id='widget-row2', component_property='style')],
    [Input(component_id='series2-radio', component_property='value'),
     Input(component_id='series-radio', component_property='value')])
def select_show2(series2_id, series_id):
    if series2_id == None:
        return [], {1: '1', 2: '2'}, 2, [1,2], True, {'visibility': 'hidden'}, {'display': 'block'}, {'display': 'none'}
    while series2_id != None:
        show_widget = []
        series2_details = ia.get_movie(series2_id)
        series2_name = series2_details['title']

        series_details = ia.get_movie(series_id)

        show_widget.append(
            html.Div([
                html.Div([
                    html.Img(
                        src = series2_details['cover url']
                    )
                ]),
                html.Div(
                    style = {
                        'width': '100%',
                    },
                    children = [
                        # Show title div
                        html.Div(
                            className='series-widget-title',
                            children = [
                                html.H2(series2_name, style = {'margin': '0'}),
                            ]
                        ),
                        html.Div(
                            className='series-widget-details',
                            children = [
                                html.H5(str(series2_details['seasons']) + " seasons "),
                                html.H5(series2_details['series years']),
                                html.H5("IMDb Score: " + str(series2_details['rating'])),
                                html.H5(id='selected_result')
                            ]
                        )
                    ]
                ) 
            ])
        )
        return show_widget, {i: 'Season {}'.format(i) for i in range(1, max(series_details['seasons'],series2_details['seasons']))}, max(series_details['seasons'],series2_details['seasons']),[1, max(series_details['seasons'],series2_details['seasons'])], False, {'visibility': 'visible'}, {'display': 'none'}, {}


# Season selection output
@app.callback(
    Output(component_id='slider-text', component_property='children'),
    [Input(component_id='season-slider', component_property='value'),
     Input(component_id='season-slider', component_property='disabled')])
def update_output(value,state):
    if state==True:
        return ''
    else:
        return 'Showing ratings from Season {0:.2g}'.format(value[0]) + ' to {0:.2g}'.format(value[1]) + '.'


# Graphing the show
@app.callback(
    [Output(component_id='ratings_graph', component_property='figure'),
     Output(component_id='search-input', component_property='value')],
    [Input(component_id='season-slider', component_property='value'),
     Input('my-toggle-switch', 'value'),
     Input(component_id='series-radio', component_property='value'),
     Input(component_id='series2-radio', component_property='value'),
     Input(component_id='season-slider', component_property='disabled'),
     Input(component_id='season2-slider', component_property='disabled')])
def plot_graph(slider_val, toggle_state, series_id, series2_id, state, state2):
    # Initialize array of series ratings
    series_details = []
    series_ratings = []
    episode_names = []
    dot_color = []
    series_season = []
    s_no = []
    e_no = []
    
    first_season = slider_val[0]
    final_season = slider_val[1]+1

    if state==False:
        series_details = ia.get_movie(series_id)
        ia.update(series_details, 'episodes')
        # Loop to assign ratings and names of all episodes within season range
        for s in range(first_season, final_season):
            try:
                series_season = series_details['episodes'][s]
            except KeyError:
                continue
            if s%2 == 0:
                this_season = '#303030'
            else:
                this_season = '#f5f5f5'
            
            for i in series_season:
                if 'rating' in series_season[i]:
                    series_ratings.append(round(series_season[i]['rating'],2))
                    episode_names.append(series_season[i]['title'])
                    dot_color.append(this_season)
                    s_no.append(s)
                    e_no.append(series_season[i]['episode'])
        
        # Graph 1
        data = [
            go.Scatter(
                # customdata = series_ratings,
                x = list(range(1,len(series_ratings)+1)),
                y = series_ratings,
                mode='lines+markers',
                line = dict(
                    width = 2,
                    color = '#000000'
                ),
                marker= dict(
                    color = pd.Series(dot_color),
                    size = 6,
                    line = dict(
                        color = '#000000',
                        width = 1
                    )
                ),
                hoverinfo='text',
                hoverlabel= dict(
                    bgcolor= '#303030',
                    bordercolor='white',
                    font=dict(
                        size=16
                    ),
                ),
                hovertext= 'S' + pd.Series(s_no).astype(str) + 'E' + pd.Series(e_no).astype(str) + '<br><b>' + pd.Series(episode_names) + '</b><br>' + 'IMDb Rating: <b>' + pd.Series(series_ratings).astype(str) + '</b>'
            )
        ]

        layout = dict(
            margin= dict(
                l=20, r=0,t=10,b=30
            ),
            xaxis=dict(
                title=dict(
                    text='Episode Number'
                )
            ),
            paper_bgcolor = '#f5f5f5',
            plot_bgcolor='#f5f5f5',
            # Checks toggle state for autoscaling
            yaxis= dict(
                range=[0,10],
                autorange = False if(toggle_state==False) else True,
                showgrid=True,
                nticks = 40 if(toggle_state==False) else 20,
                text='IMDb Score'
            ),
            dragmode=False
        )

        fig = dict(data = data, layout = layout)

        return fig, None

    else:
        return {'data':[]}, None

# Graph 2

@app.callback(
    [Output(component_id='ratings2_graph', component_property='figure'),
    Output(component_id='search-input2', component_property='value')],
    [Input(component_id='season2-slider', component_property='value'),
     Input('my-toggle-switch2', 'value'),
     Input(component_id='series-radio', component_property='value'),
     Input(component_id='series2-radio', component_property='value'),
     Input(component_id='season2-slider', component_property='disabled')])
def plot_graph2(slider_val, toggle_state, series_id, series2_id, state):
    # Initialize array of series ratings
    series_details = []
    series_ratings = []
    episode_names = []
    dot_color = []
    series_season = []
    s_no = []
    e_no = []

    series_details2 = []
    series_ratings2 = []
    episode_names2 = []
    s_no2 = []
    e_no2 = []
    dot_color2 = []
    series_season2 = []
    first_season = slider_val[0]
    final_season = slider_val[1]+1

    if state==False:
        series_details = ia.get_movie(series_id)
        ia.update(series_details, 'episodes')
        # Loop to assign ratings and names of all episodes within season range
        for s in range(first_season, final_season):
            try:
                series_season = series_details['episodes'][s]
            except KeyError:
                continue
            if s%2 == 0:
                this_season = '#303030'
            else:
                this_season = '#f5f5f5'
            
            for i in series_season:
                if 'rating' in series_season[i]:
                    series_ratings.append(round(series_season[i]['rating'],2))
                    episode_names.append(series_season[i]['title'])
                    dot_color.append(this_season)
                    s_no.append(s)
                    e_no.append(series_season[i]['episode'])

        series_details2 = ia.get_movie(series2_id)
        ia.update(series_details2, 'episodes')     

        for s in range(first_season, final_season):
            try:
                series_season2 = series_details2['episodes'][s]
            except KeyError:
                continue
            if s%2 == 0:
                this_season2 = '#A6373F'
            else:
                this_season2 = '#f5f5f5'
            
            for i in series_season2:
                if 'rating' in series_season2[i]:
                    series_ratings2.append(round(series_season2[i]['rating'],2))
                    episode_names2.append(series_season2[i]['title'])
                    dot_color2.append(this_season2)
                    s_no2.append(s)
                    e_no2.append(series_season2[i]['episode'])

        data = [
            go.Scatter(
                # customdata = series_ratings,
                x = list(range(1,len(series_ratings)+1)),
                y = series_ratings,
                name = series_details['title'],
                mode='lines+markers',
                line = dict(
                    width = 2,
                    color = '#000000'
                ),
                marker= dict(
                    color = pd.Series(dot_color),
                    size = 6,
                    line = dict(
                        color = '#000000',
                        width = 1
                    )
                ),
                hoverinfo='text',
                hoverlabel= dict(
                    bgcolor= '#303030',
                    bordercolor='white',
                    font=dict(
                        size=16
                    ),
                ),
                hovertext= 'S' + pd.Series(s_no).astype(str) + 'E' + pd.Series(e_no).astype(str) + '<br><b>' + pd.Series(episode_names) + '</b><br>' + 'IMDb Rating: <b>' + pd.Series(series_ratings).astype(str) + '</b>'
            ),
            go.Scatter(
                x = list(range(1,len(series_ratings2)+1)),
                y = series_ratings2,
                name = series_details2['title'],
                mode='lines+markers',
                line = dict(
                    width = 2,
                    color = '#A6373F'
                ),
                marker= dict(
                    color = pd.Series(dot_color2),
                    size = 6,
                    line = dict(
                        color = '#A6373F',
                        width = 1
                    )
                ),
                hoverinfo='text',
                hoverlabel= dict(
                    bgcolor= '#530006',
                    bordercolor='white',
                    font=dict(
                        size=16
                    ),
                ),
                hovertext= 'S' + pd.Series(s_no2).astype(str) + 'E' + pd.Series(e_no2).astype(str) + '<br><b>' + pd.Series(episode_names2) + '</b><br>' + 'IMDb Rating: <b>' + pd.Series(series_ratings2).astype(str) + '</b>'
            ) 
        ]

        layout = dict(
            margin= dict(
                l=20, r=0,t=10,b=30
            ),
            xaxis=dict(
                title=dict(
                    text='Episode Number'
                )
            ),
            paper_bgcolor = '#f5f5f5',
            plot_bgcolor='#f5f5f5',
            # Checks toggle state for autoscaling
            yaxis= dict(
                range=[0,10],
                autorange = False if(toggle_state==False) else True,
                showgrid=True,
                nticks = 40 if(toggle_state==False) else 20,
                text='IMDb Score'
            ),
            dragmode=False
        )

        fig = dict(data = data, layout = layout)

        return fig, None

    else:
        return {'data':[]}, None

# Populate breakdown season dropdown
@app.callback(
    Output(component_id='breakdown-season-dropdown', component_property='options'),
    [Input(component_id='series-radio', component_property='value')])
def populate_season_dropdown(series_id):
    while series_id != None:
        series_details = ia.get_movie(series_id)
        return [{'label': 'Season ' + str(i), 'value': i} for i in range(1,series_details['seasons']+1)]
    else:
        return []

# Populate breakdown episode dropdown
@app.callback(
    Output(component_id='breakdown-episode-dropdown', component_property='options'),
    [Input(component_id='breakdown-season-dropdown', component_property='value'),
     Input(component_id='series-radio', component_property='value')])
def populate_episode_dropdown(s_no, series_id):
    if series_id != None and s_no !=None:
        series_details = ia.get_movie(series_id)
        ia.update(series_details, 'episodes')
        ep_count = len(series_details['episodes'][s_no])
        return [{'label': 'Episode ' + str(i), 'value': i} for i in range(1,ep_count+1)]
    else:
        return []
    
# Populate breakdown details
@app.callback(
    [Output(component_id='breakdown-details', component_property='style'),
     Output(component_id='breakdown-episode-name', component_property='children'),
     Output(component_id='breakdown-episode-score', component_property='children'),
     Output(component_id='breakdown-episode-mean', component_property='children'),
     Output(component_id='breakdown-episode-median', component_property='children'),
     Output(component_id='breakdown-graph', component_property='figure'),
     Output(component_id='breakdown-row', component_property='style'),
     Output(component_id='breakdown-row-empty', component_property='style')],
    [Input(component_id='breakdown-season-dropdown', component_property='value'),
     Input(component_id='breakdown-episode-dropdown', component_property='value'),
     Input(component_id='series-radio', component_property='value')])
def populate_breakdown_info(s_no, e_no, series_id):
    if e_no != None:
        series_details = ia.get_movie(series_id)
        ia.update(series_details, 'episodes')
        episode_id = series_details['episodes'][s_no][e_no].movieID
        imdb_rating = ia.get_movie(episode_id)['rating']
        vote_details = ia.get_movie(episode_id, 'vote details')
        vote_count = vote_details.get('number of votes')
        score = [(x) for x,y in vote_count.items()]
        count = [(y) for x,y in vote_count.items()]
        # Bar graph

        data = [
            go.Bar(
                x=score,
                y = count,
                marker = {'color': '#7C151C'}
            )
        ]

        layout = dict(
            margin= dict(
                l=60, r=0,t=10,b=30
            ),
            xaxis=dict(
                title=dict(
                    text='IMDb Score'
                )
            ),
            height = 500,
            width = 800,
            paper_bgcolor = '#f5f5f5',
            plot_bgcolor='#f5f5f5',
            # Checks toggle state for autoscaling
            yaxis= dict(
                autorange = True,
                showgrid=True,
                nticks = 20,
                text='Number of Votes'
            ),
            dragmode=False
        )
        
        fig = dict(data = data, layout = layout)

        return {'visibility': 'visible'}, series_details['episodes'][s_no][e_no]["title"], imdb_rating, vote_details['arithmetic mean'], vote_details['median'],  fig, {'visibility': 'visible'}, {'display': 'none'}
    else:
        return {'visibility': 'hidden'}, "", "", "", "", {'data':[]}, {'visibility': 'hidden'}, {'display': 'block'}


if __name__ == '__main__':
    app.run_server(debug=True)