from flask import Flask, render_template, request, redirect, jsonify
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import compute
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)

stocks = []

def generate_pie_chart(stocks):
    portfolio = compute.create_portfolio(stocks)
    labels = list(portfolio.keys())
    values = list(portfolio.values())

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.set_title('Portfolio')
    ax.legend(labels, title='Stocks', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

    canvas = FigureCanvas(fig)
    buffer = io.BytesIO()
    canvas.print_png(buffer)

    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return chart_image

@app.route('/')
def index():
    chart_image = generate_pie_chart(stocks)
    return render_template('index.html', stocks=stocks, chart_image=chart_image)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    new_stock = request.form['stock']
    stocks.append(new_stock)
    print(stocks)
    return render_template('index.html', stocks=stocks)

@app.route('/remove_stock', methods=['POST'])
def remove_stock():
    stock_to_remove = request.form['stock']
    if stock_to_remove in stocks:
        stocks.remove(stock_to_remove)
    print(stocks)
    chart_image = generate_pie_chart(stocks)
    return render_template('index.html', stocks=stocks, chart_image=chart_image)


@app.route('/clear_stocks', methods=['POST'])
def clear_stocks():
    stocks.clear()
    print(f"stocks: {stocks}")
    chart_image = generate_pie_chart(stocks)
    return render_template('index.html', stocks=stocks, chart_image=chart_image)

@app.route('/compute')
def portfolio():
    chart_image = generate_pie_chart(stocks)
    return render_template('index.html', stocks=stocks, chart_image=chart_image)


if __name__ == '__main__':
    app.run(debug=True)
