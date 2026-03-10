from recommend import filter, tfidf_recommendation
import nltk
import time
import hashlib
import json
from functools import lru_cache
from flask import Flask, request, jsonify, make_response
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

# Pre-compute and cache the /api/data response since it never changes at runtime
_data_response = json.dumps({
    'grapes': _grapes,
    'countries': _countries,
    'types': _types,
    'categoryTastes': _categoryTastes,
    'prices': _prices,
})
_data_etag = hashlib.md5(_data_response.encode()).hexdigest()

# In-memory cache for /api/recommend results
_recommend_cache = {}
_CACHE_MAX_SIZE = 512


def _build_cache_key(req_data):
    normalized = json.dumps(req_data, sort_keys=True)
    return hashlib.md5(normalized.encode()).hexdigest()


def _serialize_results(recommended_wines_df):
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
    return results


@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    req_data = request.get_json()
    cache_key = _build_cache_key(req_data)

    if cache_key in _recommend_cache:
        return _recommend_cache[cache_key]

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

    result = {'results': _serialize_results(recommended_wines_df)}

    # Evict oldest entries if cache is full
    if len(_recommend_cache) >= _CACHE_MAX_SIZE:
        _recommend_cache.pop(next(iter(_recommend_cache)))
    _recommend_cache[cache_key] = result

    return result


@app.route('/api/data', methods=['GET'])
def get_data():
    # Return 304 if client already has current data
    if request.headers.get('If-None-Match') == _data_etag:
        return '', 304

    response = make_response(_data_response)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'public, max-age=86400'
    response.headers['ETag'] = _data_etag
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')