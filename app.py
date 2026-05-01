from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(_name_)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    symbol = ""
    if request.method == 'POST':
        symbol = request.form['symbol']
        data = yf.download(symbol, period='1y')
        
        # Simple ML: Using previous day's close to predict today's
        data['Next_Close'] = data['Close'].shift(-1)
        data.dropna(inplace=True)
        
        X = data[['Close']].values
        y = data['Next_Close'].values
        
        model = LinearRegression().fit(X[:-1], y[:-1])
        latest_price = X[-1].reshape(1, -1)
        prediction = round(float(model.predict(latest_price)[0]), 2)

    return render_template('index.html', prediction=prediction, symbol=symbol)

if _name_ == '_main_':
    app.run(debug=True)
