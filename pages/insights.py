# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Insights

            What insights can this model provide? We can take a look at a few visualizations created from the model to find out.

            First, let's take a look at the permutation importances of the model. Permutation importances are an efficient way of discovering which features your model relies most heavily upon. Essentially, each number you see below next to a feature is representative of the average amount a prediction changed after scrambling the values of only that feature across various predictions. So, if you scramble all the latitude values (thus making the value ostensibly meaningless), while keeping all other values the same, the prediction changed an average of 6.9871 +/- .4332 days. 


            """,
            style={'fontFamily':'Verdana', 'fontWeight': 'normal', 'fontSize': 'smaller'}
        ),   
        html.Div(
            html.Img(src='assets/permutation_importances.png', className='img-fluid', width=250), 
            style={'textAlign': 'center'}
        ),  
        dcc.Markdown(
            """
            We can see from these permutation importances that by far, the most important features to the model were location and the number of open cases. It's interesting to note that, although the data included several different features relative to location (council District, Police District, County, ZIP Code, etc), latitude and longitude were by far the most useful, indicating that precise location was more important than any of the other location categories could provide. In fact, when I tried to use ZIP Code instead of lat/lon in the simplified model, my R^2 score was reduced by half. 

            So how exactly is latitude and longitude impacting the model? The permutation importances only tell us that the model is using those features, but not how. I created a 2-D partial dependence interact plot (PDP) to visualize this. The easiest way to think of the PDP interact is to think: if latitude and/or longitude changes, how does the target change? The shading, as well as the numbers in the boxes, both represent the average prediction of 'days to close' based on those coordinates.

            """,
            style={'fontFamily':'Verdana', 'fontWeight': 'normal', 'fontSize': 'smaller'},
            className='mt-4'
        ),
        html.Div(
            html.Img(src='assets/pdp_2d_lat_lon_updated.png', className='img-fluid', width=550), 
            style={'textAlign': 'center'}
        ),
        dcc.Markdown(
            """
            As you can see, the darkest box, or highest prediction, is in the 39.02 lat, -94.52 long region, which is towards South Kansas City around Swope Parkway. It's important to note that, while this is interesting information, the most firm conclusion we can draw from any model analysis is what information the model finds important. We may not be able to draw solid conclusions about reality based on this. 

            But what other features can we look into? Let's look at the PDP for open cases. This visualization looks different than the previous one because it's only looking at how predictions changed based on one feature, not two. 
            """,
            style={'fontFamily':'Verdana', 'fontWeight': 'normal', 'fontSize': 'smaller'}
        ),
        html.Div(
            html.Img(src='assets/pdp_open_cases.png', className='img-fluid', width=750), 
            style={'textAlign': 'center'}
        ),
        dcc.Markdown(
            """
            Note that the y-axis on this graph is showing how a prediction changed with variance of 'open cases', not what the prediction actually was. So you can interpret this graph by seeing that, generally, this model predicted that potholes would take longer to fill the more open cases there were. However, there were some instances, between 1000-2000 and 3000-4500 most notably, where predictions decreased with an increase in open cases. This is a great example of something that is difficult to be able to derive certain meaning from, or to know why this happens, especially given that we already know that the model doesn't account for all the variance in the data. But it does explain why, on the predictions page, your prediction may go down if you toggle all the way to "Most KC has ever seen" on the 'open cases' variable's slider.  

            Last but not least, let's take a look at one individual prediction. How does the model bring all these features together to make a prediction? One of the best ways of trying to look at this is with a Shapley plot. The Shapley plot below has taken this row of input:
            """,
            style={'fontFamily':'Verdana', 'fontWeight': 'normal', 'fontSize': 'smaller'},
            className='mt-4'
        ),
        html.Div(
            html.Img(src='assets/shapley_87_row.png', className='img-fluid', width=800), 
            style={'textAlign': 'center'}
        ),
        dcc.Markdown("and visualized how the model came up with a 87.09 day prediction:", 
            className='mt-4', 
            style={'fontFamily':'Verdana', 'fontWeight': 'normal', 'fontSize': 'smaller'}
        ),
        html.Div(
            html.Img(src='assets/shapley_87.png', className='img-fluid', width=800), 
            style={'textAlign': 'center'}
        ),
        dcc.Markdown(
            """
            Think of the number line as a range of potential predictions, with the bolded number being the final prediction. All of the red factors are visualized as arrows pushing the prediction to the right, or higher. Since this prediction was rather high, you can see that there are very few factors (blue), that are pushing it lower. We can see from the size of the 'arrows' how much each factor influenced the prediction. So this prediction was made highest because of the number of open cases and the latitude. 

            Overall, while this model may not have reached as high of an R^2 score as I'd hoped, it's still interesting to take a peek inside and see how it worked with the data that it had. And of course, it's always fun to come up with alliterative synonyms for pothole to use for fun interactive predictions. 
            """,
            style={'fontFamily':'Verdana', 'fontWeight': 'normal', 'fontSize': 'smaller'},
            className='mt-4'
        )
       
  

    ],
)


layout = dbc.Row([column1])
