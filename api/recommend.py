from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import sys
import pandas as pd

def filter(df, priceMin: int = 0, priceMax: int = sys.maxsize, grapes: list = [], countries: list = [], types: list = [], taste: list = []):
  # Filter for her typical price points
  priceFilterBool = ((df.price >= priceMin) & (df.price <= priceMax))

  countryFilterBool = (df.country.isin(countries)) if len(countries) > 0 else (
      df.country.isin(list(set(df.country))))  # Filter for country

  typeFilterBool = (df.type.isin(types)) if len(types) > 0 else (
      df.type.isin(list(set(df.type))))  # Filter for type of wine(red ...)

  tasteFilterBool = (df.categoryTaste.isin(taste)) if len(taste) > 0 else (
      df.categoryTaste.isin(list(set(df.categoryTaste))))  # Filter for taste category

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

  volumeFilterBool = ((df.volume >= 700) & (
      df.volume <= 1000))  # Filter for volume

  filtered_df = df[priceFilterBool & countryFilterBool & grapesFilterBool &
                   typeFilterBool & tasteFilterBool & volumeFilterBool]  # Filtered data frame

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
  similar_indices = cosine_similarities[0].argsort()[-2:-8:-1]
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
  print(tfidf_recs['tfidf_score'])
  return tfidf_recs
