from flask import Flask, render_template, request, redirect, jsonify
import yfinance as yf
import re

app = Flask(__name__)

stocks = []

@app.route('/')
def index():
    return render_template('index.html', stocks=stocks)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    new_stock = request.form['stock']
    stocks.append(new_stock)
    return redirect('/')

@app.route('/remove_stock', methods=['POST'])
def remove_stock():
    stock_to_remove = request.form['stock']
    if stock_to_remove in stocks:
        stocks.remove(stock_to_remove)
    return redirect('/')


@app.route('/clear_stocks', methods=['POST'])
def clear_stocks():
    stocks.clear()
    return redirect('/')


@app.route('/validate_stock', methods=['POST'])
def validate_stock():
    symbol = request.form['stock']
    
    # Perform basic validation using regular expressions
    if re.match(r'^[A-Za-z0-9]+$', symbol):
        valid = True
    else:
        valid = False

    return jsonify({'valid': valid})




if __name__ == '__main__':
    app.run(debug=True)
