import os
from dash import Dash,dcc, html, Input, Output, State  # pip install dash

from langchain.indexes import VectorstoreIndexCreator
from dotenv import dotenv_values

import dash_bootstrap_components as dbc

app = Dash(__name__)

os.environ['OPENAI_API_KEY'] = dotenv_values('.env')['openai_api_key']

from langchain.document_loaders import TextLoader

maradmins = TextLoader('./MARADMINS/madmin_scrape.txt')
index = VectorstoreIndexCreator().from_loaders([maradmins])

app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Define the layout of the app
app.layout = dbc.Container([
  html.H1('Chat with HashmarkAI', className="col-md-6 offset-md-3"),

  dbc.Textarea(
    id='input-text',
    value='',
    invalid=False, size="lg", placeholder="Ask a question...",
    class_name="col-md-6 offset-md-3 w-50"
  ),
  
  dbc.Button("Submit", id='submit-button', n_clicks=0, color="primary", className="d-grid gap-2 col-6 mx-auto my-4"),

  html.Div(
    id='output-text',
    style={'whiteSpace': 'pre-line'}
  )
])

# Define the callback function
@app.callback(
  Output('output-text', 'children'),
  Input('submit-button', 'n_clicks'),
  State('input-text', 'value')
)
def update_output(n_clicks, input_text):
  if n_clicks >0:
    # Get the response from ChatGPT
    generated_text = index.query(f"{input_text}\n")

    # Return the generated text as the output
    return generated_text

if __name__ == '__main__':
  app.run_server(debug=True)