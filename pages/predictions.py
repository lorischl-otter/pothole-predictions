# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd

# Imports from this application
from app import app

# Load pipeline
from joblib import load
pipeline = load('assets/pipeline.joblib')

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Predictions

            Just as you hope will happen with your pothole, please fill in the info below.

            """
        ),

        dcc.Markdown('##### In which month are you reporting this asphalt alcove?'),
        dcc.Dropdown(
            id='month',
            options=[
                {'label': 'January', 'value': 1},
                {'label': 'February', 'value': 2},
                {'label': 'March', 'value': 3},
                {'label': 'April', 'value': 4},
                {'label': 'May', 'value': 5},
                {'label': 'June', 'value': 6},
                {'label': 'July', 'value': 7},
                {'label': 'August', 'value': 8},
                {'label': 'September', 'value': 9},
                {'label': 'October', 'value': 10},
                {'label': 'November', 'value': 11},
                {'label': 'December', 'value': 12},
            ],
            value=1,
            className='mb-4'
        ),
        dcc.Markdown('##### How many other pavement pits have you been seeing around the city?'),
        dcc.Slider(
            id='cases',
            min=0,
            max=5161,
            marks={
                0: {'label': 'None'},
                5161: {'label': 'Most KC has ever seen'}
            },
            value=0,
            className='mb-4'
        ),        
        dcc.Markdown('##### What has the temperature been like of late?'),
        dcc.Dropdown(
            id='temp',
            options=[
                {'label': 'Below freezing (frostbite is a concern)', 'value': 'below freezing'},
                {'label': 'Cold (coat weather)', 'value': 'cold'},
                {'label': 'Mild (spring weather)', 'value': 'mild'},
                {'label': 'Warm (shorts weather)', 'value': 'warm'},
                {'label': 'Hot (sunburn is a concern)', 'value': 'hot'},               
            ],
            value='below freezing',
            className='mb-4'
        ),
        dcc.Markdown('##### How much precipitation has fallen from the sky in recent days?'),
        dcc.Dropdown(
            id='precip',
            options=[
                {'label': 'None (no umbrellas needed!)', 'value': 'none'},
                {'label': 'Low (I wish I had my umbrealla one or two days', 'value': 'low'},
                {'label': 'Medium (waterproof shoes/boots would be helpful)', 'value': 'medium'},
                {'label': 'High (I have flood and/or blizzard concerns)', 'value': 'extreme'},
                
            ],
            value='none',
            className='mb-4'
        ),
        dcc.Markdown('##### Where is the driveway divet located?'),
        dcc.Markdown('Helpful hint: go to [Google Maps](https://www.google.com/maps/search/Kansas+City,+MO/@39.0918352,-94.7158007,11z), and click where the pothole is, or type in an address, to find the coordinates.'),
        dcc.Markdown('Latitude'),
        dcc.Slider(
            id='lat',
            min=38.84,
            max=39.36,
            step=.001,
            marks={n: format(n) for n in np.arange(38.85, 39.45, .1).round(decimals=2)},
            value=39.05,
            vertical=True

        ),
        dcc.Markdown('Longitude'),
        dcc.Slider(
            id='lon',
            min=-94.72,
            max=-94.38,
            step=.001,
            marks={n: format(n) for n in np.arange(-94.70, -94.30, .05).round(decimals=2)},
            value=-94.55,
            className='mb-5'
        ),
        dcc.Markdown('Note that these predictions are only rough estimates based on past available data',
            className='mb-4' 
        )

    ],
    md=6,
)

column2 = dbc.Col(
    [
        dcc.Markdown('## Predicted Time to Fill:'),
        #html.H2('Predicted Time to Fill:'),
        html.Div(
            id='prediction-content',
            #className='lead',
            title='test',
            style={
                'textAlign': 'center',
                #'color': 'blue',
                'fontSize': 72

            }
        )
    ]
)

@app.callback(
    Output('prediction-content', 'children'),
    [Input('cases', 'value'),
    Input('lat', 'value'),
    Input('lon', 'value'),
    Input('precip', 'value'),
    Input('month', 'value'),
    Input('temp', 'value')]
)
def predict(cases, lat, lon, precip, month, temp):
    df = pd.DataFrame(
        columns=['OPEN CASES',
                'LATITUDE', 
                'LONGITUDE',
                'WEEK PRECIP',
                'CREATION MONTH',
                'HI TEMP'],
        data=[[cases, lat, lon, precip, month, temp]]
    )
    y_pred=pipeline.predict(df)[0]
    y_pred_pos = np.clip(y_pred, a_min=0, a_max=250)
    if (y_pred_pos < 1.5):
        return f'{y_pred_pos:.0f} day'
    else:
        return f'{y_pred_pos:.0f} days'
 

layout = dbc.Row([column1, column2])