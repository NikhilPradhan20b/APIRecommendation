from fastapi import FastAPI
import pandas as pd
import numpy as np
import scipy.stats

#Visualization

import seaborn as sns

app = FastAPI()

@app.get("/")
def read_root():
    return {'Hello':'World'}

@app.post("/user-recommendation")
def recommend_item(data: list):
    #Read in data
    ratings = pd.read_csv('shoesdata.csv')
    for i in range(len(data)):
        ratings = ratings.append(data[i], ignore_index=True)
    print(ratings.tail())
    matrix1 = ratings.pivot_table(index='userId',columns='productId',values='Rating')
    matrix = matrix1.subtract(matrix1.mean(axis=1), axis = 'rows')
    user_similarity = matrix.T.corr()
    picked_userid = 'A061'
    user_similarity.drop(index = picked_userid,inplace=True)
    n = 5
    user_similarity_threshold = 0
    similar_users = user_similarity[user_similarity[picked_userid]>user_similarity_threshold][picked_userid].sort_values(ascending=False)[:n]
    picked_userid_watched = matrix[matrix.index == picked_userid].dropna(axis=1, how='all')
    similar_user_movies = matrix[matrix.index.isin(similar_users.index)].dropna(axis=1, how='all')
    similar_user_movies.drop(picked_userid_watched.columns,axis=1, inplace=True, errors='ignore')
    item_score = {}
    for i in similar_user_movies.columns:
        movie_rating = similar_user_movies[i]
        total = 0
        count = 0
        for u in similar_users.index:
            if pd.isna(movie_rating[u]) == False:
                score = similar_users[u] * movie_rating[u]
                total += score
                count +=1
        item_score[i] = total / count
    item_score = pd.DataFrame(item_score.items(), columns=['shoes', 'shoes_score'])
    ranked_item_score = item_score.sort_values(by='shoes_score', ascending=False)
    return ranked_item_score.head(n)

@app.get("/popularity")
def polpularity():
    ratings = pd.read_csv('shoesdata.csv')
    popular_products = pd.DataFrame(ratings.groupby('productId')['Rating'].count())
    most_popular = popular_products.sort_values('Rating', ascending=False)
    dict_from_df = most_popular.iloc[:5].to_dict()
    return dict_from_df