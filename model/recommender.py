import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("model/movies.csv")

movies["features"] = movies["title"] + " " + movies["genre"]

cv = CountVectorizer(stop_words="english")
matrix = cv.fit_transform(movies["features"])

similarity = cosine_similarity(matrix)


def recommend(search_term):
    search_term = search_term.lower()

    matches = movies[
        movies["title"].str.lower().str.contains(search_term) |
        movies["genre"].str.lower().str.contains(search_term)
    ]

    if matches.empty:
        return [("Movie not found!", "https://via.placeholder.com/300x450?text=No+Image")]

    index = matches.index[0]

    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []

    for i in movies_list:
        row = movies.iloc[i[0]]
        title = row["title"]
        poster = row.get("poster", "https://via.placeholder.com/300x450?text=No+Image")

        recommended_movies.append((title, poster))

    return recommended_movies
