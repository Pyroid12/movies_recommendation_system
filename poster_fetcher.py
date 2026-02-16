import pandas as pd
import requests
import os
from urllib.parse import quote

api_key = os.getenv("TMDB_API_KEY")

movies = pd.read_csv("model/movies.csv")

posters = []

for title in movies["title"]:
    encoded_title = quote(title)

    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={encoded_title}&include_adult=false"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_url = "https://via.placeholder.com/300x450?text=No+Image"

        if data.get("results"):
            sorted_results = sorted(
                data["results"],
                key=lambda x: x.get("popularity", 0),
                reverse=True
            )

            for movie in sorted_results:
                if movie.get("poster_path"):
                    poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                    break

        posters.append(poster_url)

    except:
        posters.append("https://via.placeholder.com/300x450?text=No+Image")

movies["poster"] = posters
movies.to_csv("model/movies.csv", index=False)

print("Posters saved successfully!")
