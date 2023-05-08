# Content Based Filtering - TMDB 5000 Movie Dataset
# Ever Alvarez - 8A

import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# ______________________________________________________________________________________________________________________

def load_data(movies_file_path, credits_file_path):
    movies = pd.read_csv(movies_file_path)
    credits = pd.read_csv(credits_file_path)
    return movies.merge(credits, on='title')

def preprocess_data(data):
    data = data.loc[:, ['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew', 'vote_average', 'vote_count']]
    data.dropna(inplace=True)
    data['genres'] = data['genres'].apply(lambda x: [genre['name'].replace(" ", "") for genre in ast.literal_eval(x)])
    data['keywords'] = data['keywords'].apply(lambda x: [keyword['name'].replace(" ", "") for keyword in ast.literal_eval(x)])
    data['cast'] = data['cast'].apply(lambda x: [actor['name'].replace(" ", "") for actor in ast.literal_eval(x)])
    data['cast'] = data['cast'].apply(lambda x: x[0:3])
    data['crew'] = data['crew'].apply(lambda x: [member['name'].replace(" ", "") for member in ast.literal_eval(x) if member['job'] == 'Director'])
    data['overview'] = data['overview'].apply(lambda x: x.split())
    data['tags'] = data['overview'] + data['genres'] + data['keywords'] + data['cast'] + data['crew']
    data.drop(columns=['overview', 'genres', 'keywords', 'cast', 'crew'], inplace=True)
    data.loc[:, 'tags'] = data['tags'].apply(lambda x: " ".join(x))
    return data

def compute_similarity_matrix(data):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(data['tags']).toarray()
    return cosine_similarity(vector)

def get_recommendations(movie_id, data, similarity_matrix, num_recommendations=5):
    indices = pd.Series(data.index, index=data['title'])
    index = indices[movie_id]
    similarity_scores = list(enumerate(similarity_matrix[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:num_recommendations+1]
    movie_indices = [i[0] for i in similarity_scores]
    return data[['title', 'vote_average', 'vote_count']].iloc[movie_indices]

def dump_model(preprocessed_data, similarity_matrix):
    pickle.dump(preprocessed_data,open('movie_list.pkl','wb'))
    pickle.dump(similarity_matrix,open('similarity.pkl','wb'))

# ______________________________________________________________________________________________________________________

print("Loading...\n")
movies = load_data('./tmdb_5000_movies.csv', './tmdb_5000_credits.csv')
preprocessed_data = preprocess_data(movies)
similarity_matrix = compute_similarity_matrix(preprocessed_data)
dump_model(preprocessed_data, similarity_matrix)

recommendations = get_recommendations('The Lego Movie', preprocessed_data, similarity_matrix)
print(recommendations)