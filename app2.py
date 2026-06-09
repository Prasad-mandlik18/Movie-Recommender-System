import pickle
import pandas as pd
import streamlit as st
import requests

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Movie Recommender System",

)

# -----------------------------
# Fetch Poster
# -----------------------------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"

        return None

    except Exception:
        return None


# -----------------------------
# Recommend Movies
# -----------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_names.append(
            movies.iloc[i[0]].title
        )

        recommended_movie_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movie_names, recommended_movie_posters


# -----------------------------
# Load Data
# -----------------------------
@st.cache_resource
def load_data():
    movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
    movies_df = pd.DataFrame(movies_dict)

    similarity_matrix = pickle.load(open("similarity.pkl", "rb"))

    return movies_df, similarity_matrix


movies, similarity = load_data()

# -----------------------------
# UI
# -----------------------------
st.title(" Movie Recommender System")

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].tolist()
)

# -----------------------------
# Show Recommendations
# -----------------------------
if st.button("Show Recommendation"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for idx in range(len(names)):

        with cols[idx]:
            st.markdown(f"**{names[idx]}**")

            if posters[idx]:
                st.image(posters[idx], use_container_width=True)
            else:
                st.warning("Poster Not Available")


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Made with 💻 by Prasad Mandlik | Movie Recommender System
    </div>
    """,
    unsafe_allow_html=True
)