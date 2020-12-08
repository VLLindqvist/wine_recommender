from recommend import filter, tfidf_recommendation
import nltk
import time
from flask import Flask, request
import sys
import pandas as pd
import numpy as np
import seaborn as sns
sns.set()

pd.options.mode.chained_assignment = None

nltk.download('stopwords')

df_wine = pd.read_csv('systembolaget.csv', encoding="ISO-8859-1")

_grapes = []
for i in range(len(df_wine.grapes)):
    if str(df_wine.grapes[i]) != 'nan':
        _grapesList = df_wine.grapes[i].split('---')
        for grape in _grapesList:
            if grape not in _grapes:
                _grapes.append(grape)
_grapes.sort()

_countries = []
for i in range(len(df_wine.country)):
    if str(df_wine.country[i]) != 'nan':
        if str(df_wine.country[i]) not in _countries:
            _countries.append(str(df_wine.country[i]))
_countries.sort()

_types = []
for i in range(len(df_wine.type)):
    if str(df_wine.type[i]) != 'nan':
        if str(df_wine.type[i]) not in _types:
            _types.append(str(df_wine.type[i]))
_types.sort()

_categoryTastes = []
for i in range(len(df_wine.categoryTaste)):
    if str(df_wine.categoryTaste[i]) != 'nan':
        if str(df_wine.categoryTaste[i]) not in _categoryTastes:
            _categoryTastes.append(str(df_wine.categoryTaste[i]))
_categoryTastes.sort()

_prices = [sys.maxsize, 0]
for i in range(len(df_wine.price)):
    if str(df_wine.price[i]) != 'nan':
        if int(df_wine.price[i]) < _prices[0]:
            _prices[0] = int(df_wine.price[i])
        elif int(df_wine.price[i]) > _prices[1]:
            _prices[1] = int(df_wine.price[i])


app = Flask(__name__)


@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    req_data = request.get_json()
    # print(req_data['countries'])
    filtered_df = filter(
        df_wine,
        priceMin=req_data['priceLow'],
        priceMax=req_data['priceHigh'],
        grapes=req_data['grapes'],
        countries=req_data['countries'],
        types=req_data['types'],
        taste=req_data['categoryTastes']
    )

    recommended_wines_df = tfidf_recommendation(filtered_df, req_data['tasteDescription']) if (
        req_data['tasteDescription'] != "") else filtered_df.head(6)

    print(recommended_wines_df)

    results = []
    for i, rec in recommended_wines_df.iterrows():
        results.append({
            'nameBold': "" if str(rec['nameBold']) == 'nan' else rec['nameBold'],
            'nameThin': "" if str(rec['nameThin']) == 'nan' else rec['nameThin'],
            'producer': "" if str(rec['producer']) == 'nan' else rec['producer'],
            'imageURL': "" if str(rec['imageURL']) == 'nan' else rec['imageURL'],
            'url': "" if str(rec['url']) == 'nan' else rec['url'],
            'price': "" if str(rec['price']) == 'nan' else rec['price'],
            'type': "" if str(rec['type']) == 'nan' else rec['type'],
            'country': "" if str(rec['country']) == 'nan' else rec['country'],
            'region': "" if str(rec['region']) == 'nan' else rec['region'],
            'district': "" if str(rec['district']) == 'nan' else rec['district'],
            'alcoholPercentage': "" if str(rec['alcoholPercentage']) == 'nan' else rec['alcoholPercentage'],
            'tasteDescription': "" if str(rec['taste']) == 'nan' else rec['taste'],
            'tfidf_score': rec['tfidf_score'] if ('tfidf_score' in rec and str(rec['tfidf_score']) != 'nan') else 0,
        })

    return {'results': results}


@app.route('/api/data', methods=['GET'])
def get_data():
    return {
        'grapes': _grapes,
        'countries': _countries,
        'types': _types,
        'categoryTastes': _categoryTastes,
        'prices': _prices,
    }
