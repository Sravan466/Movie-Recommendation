import streamlit as st
import pickle
import requests
from streamlit.components.v1 import html

# Function to fetch movie posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/300x450?text=No+Image"

# Load movie data and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

movies_list = movies['title'].values

# App title and styles
st.set_page_config(page_title="Movie Recommender System", page_icon="🎥", layout="wide")
st.markdown("<style>body {font-family: 'Arial', sans-serif;}</style>", unsafe_allow_html=True)

st.title("🎬 Movie Recommender System")
st.subheader("Find similar movies based on your favorite!")

# Dropdown for movie selection
selected_movie = st.selectbox("Select a movie:", movies_list)

# Recommendation logic
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommend_movies = []
        recommend_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommend_movies.append(movies.iloc[i[0]].title)
            recommend_posters.append(fetch_poster(movie_id))
        return recommend_movies, recommend_posters
    except Exception as e:
        st.error(f"Error: {e}")
        return [], []

# Show recommendations when button is clicked
if st.button("Show Recommendations"):
    recommended_movies, recommended_posters = recommend(selected_movie)
    if recommended_movies:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.image(recommended_posters[i], caption=recommended_movies[i], use_column_width=True)
    else:
        st.warning("No recommendations available for this movie.")

# Footer
st.markdown("---")
st.markdown("© 2024 Movie Recommender System. Powered by Streamlit.")
