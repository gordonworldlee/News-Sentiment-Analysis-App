import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

def action(numb):
    number = int(numb)
    browser = webdriver.Chrome()

    browser.get("https://news.yahoo.com/")
    last_height = browser.execute_script("return document.body.scrollHeight")
    titles = []
    count = number
    while len(titles) < count:
        # Action scroll down
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        post_elems = browser.find_elements(By.TAG_NAME, "h3")
        elements = []
        for post in post_elems:
            if post.text != '':
                try:
                    elements.append([post.text, post.find_element(By.TAG_NAME, 'a').get_attribute('href')]) 
                except:
                    pass
    
        titles = elements
       

    df = pd.DataFrame(titles, columns=['Title', 'Links'])
    if (len(df.index) > number):
        df.drop(df.index[number:len(df.index)], inplace=True)
    
    return df

def sentiment(df):
    vader = SentimentIntensityAnalyzer()

    f = lambda title: vader.polarity_scores(title)['compound']
    df['score'] = df['Title'].apply(f)


def positive(df):
    sentiment(df)
    df = df.drop(df[df['score'] <= 0.5].index)
    return df

def negative(df):
    sentiment(df)
    df = df.drop(df[df['score'] >= -0.5].index)
    return df