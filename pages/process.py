# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown("## Process"),
        dcc.Markdown(
            """
            The winter of 2018-2019 was a rough one for Kansas City that lead to thousands of potholes across the city’s streets. It became a conversation topic everyone was familiarly frustrated with (especially those whose cars were damaged as a result). Potholes even became a hot button issue in the 2019 mayoral race, making an appearance on several mailers. (Fortunately they’re now mostly filled, thanks to the Public Works department!)

            The city of Kansas City (Missouri) has a wealth of publicly available data [here](https://data.kcmo.org), including 311 data — reports made to the city by citizens, including about things like potholes. Upon discovering this, I became instantly curious as to whether I could predict how long it would take for a pothole to be filled in the city. Did location matter? Weather? The number of potholes already reported? 

            I pulled data from the website, deciding to pull one year’s worth of data, beginning from the first freeze of 2018: October 15. I also pulled custom weather data from [NOAA’s Online Climate Data](https://www.ncdc.noaa.gov/cdo-web/search), including temperature and precipitation information from the same time period. I split the data randomly into test and training sets (with the intention of using cross-validation with my model). *
            
            """,
            style={'fontFamily':'Verdana', 'fontWeight': 'normal', 'fontSize': 'smaller'}
        ),
        html.Div(
            html.Img(src='assets/kc_by_potholes.png', className='img-fluid', width=500), 
            style={'textAlign': 'center'}
        ),
        dcc.Markdown(

            """

            (in the above image, you can see Kansas City as mapped out by its pothole reports from this time period, using latitude and longitude of all reports)

            It was easy to pick the target for my prediction. This data had a convenient column called: “Days to Close”. Given that this was a continuous numerical value, given in days, I needed to approach this as a regression problem (as opposed to classification problem, in which I would be trying to predict a category rather than a number, to say it simply). To determine the effectiveness of my prediction model, I selected R^2 score and mean absolute error (MAE) The R^2 score provides an insight into what percentage of the variance in data that your model is able to account for (helpful to see how much information you might be missing from your model), and the mean absolute error provides information on how far off, on average, a model’s predictions are from the actual data. I selected these two metrics for their intuitiveness and readability, so I could easily see and be able to explain how my model performed. 


            My baseline statistics for the data (i.e., what metrics you would get if you just guessed the average amount of ‘days to close’ for every instance) were, for a mean of 39.77 days to close:\n
            * R^2: 0 (the baseline R^2 is always zero, since simply guessing the average accounts for 0% of the variance in data)
            * MAE: 30.37 days

            Meaning, if I was able to achieve a positive R^2 score, and a MAE less than 30.37, my model could be considered a moderate success. 

            In order to clean the data and attempt to make it usable, I had to create some new features, or columns, including: the amount of precipitation in the week preceding the report, whether or not the temperature had dropped below freezing in the week before the report, how many open pothole reports there were at the time a report came in, and whether the pothole was located in one of the neighborhoods with the top five number of potholes reported. I also made sure to narrow down the data to the cases that had already been resolved (so I would actually have my target information), excluded any latitudes and longitudes outside of the KC area, and eliminated any requests that had been closed after 0 days, to eliminate any reports that had been closed immediately due to being out of area or duplicated. I dropped some other unhelpful columns, and also eliminated several columns that would have introduced leakage into my model (or information that would not be available at the time a prediction was being made) — namely information about when the report was closed, and whether it had exceeded the estimated timeframe. 

            I fit a linear regression model to attempt to improve upon my baseline, and chose a Poisson Regression, so I would not get any negative predictions (since a pothole you would be reporting would not have been already filled, negative days ago). This improved my baseline scores, but not by much. 

            * Poisson Regression R^2: .1415, (14.25%)
            * Poisson MAE: 25.72 days

            I then fit a tree-based gradient-boosted model: XGBoost. I used cross-validation as well as hyperparameter tuning and early stopping, to avoid over-fitting (and a whole lot of guessing and checking trying out different features). Ultimately, I was able to get a successful model on the training data, that still had a very improved R^2 score on the test data, even though it wasn’t as high as I was hoping. 
            
            
            * Train XGBoost R^2 Score: .90 (90%)
            * Train XGBoost MAE: 7.34 days


            * Test XGBoost R^2 Score: .3774 (37.74%)
            * Test XGBoost MAE: 18.72 days

            Given that, with the data I had, my best model was only able to account for around 38% of new data, and has an average error of almost 19 days, it’s clear that a lot more work would need to be done, or other data to be gathered, in order to come up with a model that could be considered more likely to be accurate. Therefore, this model is not useful if someone is looking for precise accuracy for when the pothole outside their house will be filled. But it can be used to gain other insights into trends in the data (see the [Insights](http://kc-pothole-predictions.herokuapp.com/insights) page).

            And finally, I created a more simplified version of my model for use in this web app, utilizing only the six features you can toggle on the [Predictions](http://kc-pothole-predictions.herokuapp.com/predictions) page, rather than the full 15 used in my full model. However, the R^2 score for this simplified model was only reduced by about 3%, to 34.64%. (MAE=19.65 days).
            &nbsp;

            &nbsp;
            
            &nbsp;

            *I first tried using a time-based split; however, since the time period with the worst potholes was so drastically different, I was unable to successfully get a positive R^2 value when applying a model to the test data from later in the year, and I decided to use a random split instead. Ideally, a time-based split would be the best for this kind of data, so it could be made more likely to be generalizable to future data, but for the purposes of this project I continued with the random split.


            """,
            style={'fontFamily':'Verdana', 'fontWeight': 'normal', 'fontSize': 'smaller'}
        ),

    ],
)

layout = dbc.Row([column1])