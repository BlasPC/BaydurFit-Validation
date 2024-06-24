from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
import numpy as np
import json
import plotly
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_plot')
def get_plot():
    filename = '/Users/juanblasperedocamio/Downloads/01-24-06-01.txt'
    df = pd.read_csv(filename, sep='\t', skiprows=5)

    time = df['Time']
    signal1 = df['Paw']
    signal2 = df['Pes']
    signal3 = df['Ptpulm']
    cut = True
    if cut:
        ti = 400
        tf = 460
        fs = 256
        time = df['Time'][ti*fs:tf*fs]
        signal1 = df['Paw'][ti*fs:tf*fs]
        signal2 = df['Pes'][ti*fs:tf*fs]
        signal3 = df['Ptpulm'][ti*fs:tf*fs]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=signal1, mode='lines', name='Paw[cmH2O]'))
    fig.add_trace(go.Scatter(x=time, y=signal2, mode='lines', name='Pes[cmH2O]'))
    fig.add_trace(go.Scatter(x=time, y=signal3, mode='lines', name='Ptpulm[cmH2O]'))

    fig.update_layout(
        title='Respiratory Signals',
        xaxis_title='Time',
        yaxis_title='[cmH2O]',
        dragmode='select',
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(f"Received data: {data}")
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
