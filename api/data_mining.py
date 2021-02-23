import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import pandas as pd

def insertReviews(df_wines, df_reviews):
  # Initialize a TFIDF Vectorizer model to work with the text data
  tf = TfidfVectorizer(analyzer='word', min_df=0)

  # =========== Fill empty columns in both dataframes ===========
  df_wines["nameBold"] = df_wines["nameBold"].fillna('')
  df_wines["nameThin"] = df_wines["nameThin"].fillna('')
  df_wines["country"] = df_wines["country"].fillna('')
  df_wines["producer"] = df_wines["producer"].fillna('')
  df_wines["region"] = df_wines["region"].fillna('')
  df_wines["district"] = df_wines["district"].fillna('')
  df_wines["grapes"] = df_wines["grapes"].fillna('')
  
  df_reviews["title"] = df_reviews["title"].fillna('')
  df_reviews["country"] = df_reviews["country"].fillna('')
  df_reviews["winery"] = df_reviews["winery"].fillna('')
  df_reviews["variety"] = df_reviews["variety"].fillna('')
  df_reviews["province"] = df_reviews["province"].fillna('')
  df_reviews["region_1"] = df_reviews["region_1"].fillna('')
  df_reviews["region_2"] = df_reviews["region_2"].fillna('')
  df_reviews["points"] = df_reviews["points"].fillna('')
  # =============================================================

  # ============ Concat all desired string into one =============
  wine_strings = list(df_wines['nameBold'].astype(str)
  + " " + df_wines["nameThin"].astype(str)
  + " " + df_wines["country"].astype(str)
  + " " + df_wines["producer"].astype(str)
  + " " + df_wines["region"].astype(str)
  + " " + df_wines["district"].astype(str)
  + " " + df_wines["grapes"].astype(str))

  review_strings = list(df_reviews['title'].astype(str)
  + " " + df_reviews["country"].astype(str)
  + " " + df_reviews["winery"].astype(str)
  + " " + df_reviews["variety"].astype(str)
  + " " + df_reviews["province"].astype(str)
  + " " + df_reviews["region_1"].astype(str)
  + " " + df_reviews["region_2"].astype(str)
  + " " + df_reviews["points"].astype(str))
  # =============================================================

  for wine_string in wine_strings:
    # Use the initiated TFIDF model to transform the data in the concatenated strings
    current_review_strings = review_strings
    current_review_strings.insert(0, wine_string)

    tfidf_matrix = tf.fit_transform(current_review_strings)

    # Compute the cosine similarities between the items in the newly transformed TFIDF matrix
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
    print(cosine_similarities)

  # # Extract the top 5 wines (last number inside [] reverses the list)
  # similar_indices = cosine_similarities[0].argsort()[-2:-8:-1]
  # similar_items = [(cosine_similarities[0][i], df.reset_index()['index'][i-1])
  #                  for i in similar_indices]  # Find the TFIDF score of that item

  # tfidf_recs = pd.DataFrame()

  # # Iterate over the similar items' indices and add to dataframe
  # for item in similar_items:
  #   tfidf_recs = tfidf_recs.append(df[df.index.isin([item[1]])])

  # tfidf_scores = []

  # # Iterate through the data frame of recommended wines to find their TFIDF scores and add that to the data frame
  # for i in tfidf_recs.index:
  #   for item in similar_items:
  #     if i == item[1]:
  #       tfidf_scores.append(item[0])

  # tfidf_recs['tfidf_score'] = tfidf_scores
  # print(tfidf_recs['tfidf_score'])
  # return tfidf_recs


# =========================== MAIN ===========================

pd.options.mode.chained_assignment = None

df_wines = pd.read_csv('systembolaget_raw.csv', encoding="ISO-8859-1")
df_reviews = pd.read_csv('winemag-data-130k-v2.csv', encoding="utf-8")

insertReviews(df_wines, df_reviews)