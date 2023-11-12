# app.py
from flask import Flask, render_template
import plotly.express as px
import pandas as pd
import plotly
import json


app = Flask(__name__)

@app.route('/')
def index():
    # Create a Plotly figure (replace this with your actual data)
    
    df = pd.read_csv('./static/hydrants.csv')
    color_scale = {'not ok': 'red', 'ok': 'green', 'needs testing': 'yellow'} 

    fig = px.scatter_mapbox(df, 
                            lat="latitude", 
                            lon="longitude", 
                            hover_name="status", 
                            hover_data=["status", "pressure"],
                            color='status',
                            color_discrete_map=color_scale,  # Specify color scale
                            zoom=8, 
                            height=800,
                            width=800)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Update legend
    fig.update_traces(marker=dict(size=10))  # Adjust marker size as needed
    fig.update_layout(legend_title_text='status')

    # Convert the Plotly figure to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
