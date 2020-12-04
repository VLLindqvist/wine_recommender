from nltk.corpus import stopwords
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from flask import Flask, request
import sys
import pandas as pd
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
  print(req_data['test'])

  def filter(df, priceMin: int = 0, priceMax: int = sys.maxsize, grapes: list = None, countries: list = None, types: list = None, taste: list = None):
    # Filter for her typical price points
    priceFilterBool = ((df.price >= priceMin) & (df.price <= priceMax))

    countryFilterBool = (df.country.isin(countries)) if countries != None else (
        df.country.isin(list(set(df.country))))  # Filter for country

    typeFilterBool = (df.type.isin(types)) if types != None else (
        df.type.isin(list(set(df.type))))  # Filter for country

    tasteFilterBool = (df.categoryTaste.isin(taste)) if taste != None else (
        df.categoryTaste.isin(list(set(df.categoryTaste))))  # Filter for country

    grapesFilterBool = (df.grapes.isin(list(set(df.grapes))))
    if len(grapes) > 0:
      grapesFilterBool = (~df.grapes.isin(list(set(df.grapes))))
      print(grapesFilterBool)
      for i in range(len(df.grapes)):
        if str(df.grapes[i]) != 'nan':
          isInList = False
          for grape in grapes:
            isInList = (grape in df.grapes[i]) if isInList == False else True

          grapesFilterBool[i] = isInList

    filtered_df = df[priceFilterBool & countryFilterBool & grapesFilterBool &
                     typeFilterBool & tasteFilterBool]  # Filtered data frame

    # Sort/group by wine type then price
    filtered_df.sort_values(by=['price'], ascending=True, inplace=True)

    return filtered_df

  def tfidf_recommendation(df, inputTasteDescr: str = ""):
    # Initialize a TFIDF Vectorizer model to work with the text data
    tf = TfidfVectorizer(analyzer='word',
                         min_df=0,
                         stop_words=list(set(stopwords.words('swedish'))))

    # Use the initiated TFIDF model to transform the data in descriptions
    df["taste"] = df["taste"].fillna('')
    tasteDescriptionsRaw = df.taste
    tasteDescriptions = []
    for descr in tasteDescriptionsRaw:
      tasteDescriptions.append(descr)

    tasteDescriptions.insert(0, inputTasteDescr)

    tfidf_matrix = tf.fit_transform(tasteDescriptions)

    # Compute the cosine similarities between the items in the newly transformed TFIDF matrix
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Extract the top 5 wines (last number inside [] reverses the list)
    similar_indices = cosine_similarities[0].argsort()[-2:-7:-1]
    similar_items = [(cosine_similarities[0][i], df.reset_index()['index'][i-1])
                     for i in similar_indices]  # Find the TFIDF score of that item

    tfidf_recs = pd.DataFrame()

    # Iterate over the similar items' indices and add to dataframe
    for item in similar_items:
      tfidf_recs = tfidf_recs.append(df[df.index.isin([item[1]])])

    tfidf_scores = []

    # Iterate through the data frame of recommended wines to find their TFIDF scores and add that to the data frame
    for i in tfidf_recs.index:
      for item in similar_items:
        if i == item[1]:
          tfidf_scores.append(item[0])

    tfidf_recs['tfidf_score'] = tfidf_scores

    return tfidf_recs

  # print(tfidf_recommendation(df_wine, ""))
  return {'time': time.time()}


@app.route('/api/data', methods=['GET'])
def get_data():
  return {
      'grapes': _grapes,
      'countries': _countries,
      'types': _types,
      'categoryTastes': _categoryTastes,
      'prices': _prices,
  }
