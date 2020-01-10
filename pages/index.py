# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ### How long will that pothole take to fill?
            
            
            If you live in Kansas City, or know anyone who does, you know that potholes were a major issue in Winter 2019. People even [threw birthday parties](https://www.cnn.com/2019/07/01/us/man-threw-birthday-party-for-3-month-old-pothole-trnd/index.html) for their potholes.

            This app allows you to input some basic information and recieve a prediction for how long a given pothole might take to fill in Kansas City, Missouri.
            """
        ),
        dcc.Link(dbc.Button('Fill That Pothole', color='primary'), href='/predictions'),

    ],
    md=6,
)

column2 = dbc.Col(
    [
        html.Img(src='assets/pothole_cake.jpeg', className='img-fluid'),

    ]
)



layout = dbc.Row([column1, column2])