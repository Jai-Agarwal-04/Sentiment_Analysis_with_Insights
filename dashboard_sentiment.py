#Importing all the necessary Libraries
import pickle
import pandas as pd
import webbrowser
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import base64
from dash.dependencies import Input, Output, State
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
project_name = "Sentiment Analysis with Insights"

#Declarling the Variable for the IMG to be displayed
global image_filename 
image_filename = 'pie_plot.png'
global image_filename_2 
image_filename_2 = 'wordCloud.png'
global encoded_image 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
global encoded_image_2 
encoded_image_2 = base64.b64encode(open(image_filename_2, 'rb').read())

#Working with function 
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

def load_model():
    global pickle_model
    global vocab
    global scrappedReviews
    
    scrappedReviews = pd.read_csv('Final_Etsy_Screapped_Reviews.csv')
    file = open("pickle_model.pkl", 'rb') 
    pickle_model = pickle.load(file)

    file = open("feature.pkl", 'rb') 
    vocab = pickle.load(file)

def check_review(reviewText):
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    return pickle_model.predict(reviewText)

# Start of Web UI
def create_app_ui():
    global project_name
    main_layout = dbc.Container(
        
        dbc.Jumbotron(
                [
                    html.H1(id = 'heading', children = project_name, className = 'display-3 mb-4'),
                    html.H3(id = 'heading_pie', children = 'A Pie-Chart Representation of Outcomes',className = 'display-6 mb-7',
                            style = {'margin-top': '30px','margin-bottom': '15px'}),
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style = {'margin-bottom': '30px'}),
                    html.H3(id = 'heading_word_cloud', children = 'Maximum used words as WordCloud',className = 'display-6 mb-7',
                            style = {'margin-top': '30px','margin-bottom': '15px'}),
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image_2.decode()),style = {'margin-bottom': '30px'}),
                    dbc.Container([
                            dcc.Dropdown(
                    id='dropdown',
                    placeholder = 'Select a Review',
                    options=[{'label': i[:60] + "...", 'value': i} for i in scrappedReviews.reviews[:1000]],
                    value = scrappedReviews.reviews[0],
                    style = {'margin-bottom': '30px'}
                    
                )
                       ],
                        style = {'padding-left': '50px', 'padding-right': '50px'}
                        ),
                    dbc.Button("Submit", color="dark", className="mt-2 mb-3", id = 'button', style = {'width': '100px'}),
                    html.Div(id = 'result1'),
                    dbc.Textarea(id = 'textarea', className="mb-3", placeholder="Enter the Review", value = '', style = {'height': '150px'}),
                    dbc.Button("Submit", color="dark", className="mt-2 mb-3", id = 'button_2', style = {'width': '100px'}),
                    html.Div(id = 'result')
                    ],
                className = 'text-center'
                ),
        className = 'mt-4'
        )
    
    return main_layout
# Starting with the interactive part
@app.callback(
    Output('result', 'children'),
    [
    Input('button_2', 'n_clicks')
    ],
    [
    State('textarea', 'value')
    ]
    )    
def update_app_ui(n_clicks, textarea):
    result_list = check_review(textarea)
    if n_clicks >0:
        if (result_list[0] == 0 ):
            return dbc.Alert("Negative", color="danger")
        elif (result_list[0] == 1 ):
            return dbc.Alert("Positive", color="success")
        else:
            return dbc.Alert("Unknown", color="dark")

@app.callback(
    Output('result1', 'children'),
    [
    Input('button', 'n_clicks')
    ],
    [
     State('dropdown', 'value')
     ]
    )
def update_dropdown(n_clicks, value):
    result_list = check_review(value)
    if n_clicks >0:
        if (result_list[0] == 0 ):
            return dbc.Alert("Negative", color="danger")
        elif (result_list[0] == 1 ):
            return dbc.Alert("Positive", color="success")
        else:
            return dbc.Alert("Unknown", color="dark")

#defining the main function
def main():
    global app
    global project_name
    load_model()
    #open_browser()
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server()
    app = None
    project_name = None

#Calling the main function
if __name__ == '__main__':
    main()
