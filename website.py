from flask import Flask, render_template, request
from selenium.webdriver.common.by import By
from selenium import webdriver
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from news import action, positive, sentiment, negative

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():   
    return render_template('index.html')

@app.route('/result', methods= ['POST', 'GET'])
def result():   
    if request.method == 'POST' and request.form['number'] != '' and request.form['file_submit'] == 'All':
        numb = request.form['number']
        name = action(numb)
        return render_template('base.html', tables=[name.to_html()], titles=[''])
    elif request.method == 'POST' and request.form['number'] != '' and request.form['file_submit'] == 'Positive': 
        numb = request.form['number']
        name = action(numb)
        name = positive(name)
        return render_template('base.html', tables=[name.to_html()], titles=[''])
    elif request.method == 'POST' and request.form['number'] != '' and request.form['file_submit'] == 'Negative': 
        numb = request.form['number']
        name = action(numb)
        name = negative(name)
        return render_template('base.html', tables=[name.to_html()], titles=[''])    
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
