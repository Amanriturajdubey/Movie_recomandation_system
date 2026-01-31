
import streamlit as st
import pickle
import pandas as pd
import requests

# ---------------------------
# Fetch poster and movie details from TMDB
# ---------------------------
TMDB_API_KEY = '0a26ac8256993454182e6bb7393b887c'

def fetch_movie_data(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
        response = requests.get(url)
        data = response.json()
        results = data.get('results')
        if results:
            movie = results[0]
            poster_path = movie.get('poster_path')
            poster_url = "https://image.tmdb.org/t/p/w500" + poster_path if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
            year = movie.get('release_date', '')[:4] if movie.get('release_date') else 'N/A'
            rating = movie.get('vote_average', 'N/A')
            return poster_url, year, rating
    except:
        pass
    return "https://via.placeholder.com/500x750?text=No+Image", 'N/A', 'N/A'

# ---------------------------
# Load ML data
# ---------------------------
movies = pickle.load(open('movie.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------------------
# Recommendation function
# ---------------------------
def recommend(movie_name):
    matched_movies = movies[movies['title'].str.lower() == movie_name.lower()]
    if len(matched_movies) == 0:
        st.error("Movie not found!")
        return []

    movie_index = matched_movies.index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended = []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        poster, year, rating = fetch_movie_data(title)
        recommended.append({"title": title, "poster": poster, "year": year, "rating": rating})
    return recommended

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="🎬 Cinematic Movie Recommender", layout="wide", page_icon="🎬")

st.markdown("""
<style>
/* ------------------ Overall background ------------------ */
.stApp {
    background: linear-gradient(135deg, #0B0C10, #1F1F1F);
    color: #fff;
    font-family: 'Arial', sans-serif;
}

/* ------------------ Title animations ------------------ */
@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}
.animated-title {
    animation: fadeInUp 1s ease forwards;
}
.animated-subtitle {
    animation: fadeInUp 1.5s ease forwards;
    color: #FFD700;
}

/* ------------------ Movie card ------------------ */
.movie-card {
    border-radius: 15px;
    overflow: hidden;
    text-align: center;
    margin-bottom: 30px;
    transition: transform 0.3s, box-shadow 0.3s;
    background: #1A1A1A;
    padding: 5px;
}
.movie-card:hover {
    transform: scale(1.1);
    box-shadow: 0 15px 35px rgba(255, 69, 0, 0.8);
}
.movie-title {
    font-weight: bold;
    font-size: 18px;
    margin-top: 8px;
    color: #FFD700;
    animation: fadeInUp 1.2s ease forwards;
}
.movie-subtitle {
    font-size: 15px;
    color: #ccc;
    margin-bottom: 12px;
    animation: fadeInUp 1.4s ease forwards;
}

/* ------------------ Button ------------------ */
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
    40% {transform: translateY(-8px);}
    60% {transform: translateY(-4px);}
}
.stButton > button {
    background: linear-gradient(90deg, #FF4500, #FFA500);
    color: black;
    font-weight: bold;
    border-radius: 15px;
    padding: 15px 35px;
    font-size: 18px;
    transition: background 0.3s, transform 0.3s;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #FFA500, #FF4500);
    transform: scale(1.08);
    animation: bounce 0.5s;
}

/* ------------------ Searchbox styling ------------------ */
.css-1kyxreq { width: 100% !important; }
.stSelectbox > div > div > div > span {
    font-size: 18px !important;
}

/* ------------------ Footer ------------------ */
footer { visibility: hidden; }
.custom-footer {
    text-align: center;
    color: #FFD700;
    margin-top: 50px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Page Title ------------------
st.markdown("<h1 class='animated-title'>🎬 Cinematic Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='animated-subtitle'>Discover your next favorite movie with style!</h3>", unsafe_allow_html=True)

# ------------------ Searchbar ------------------
selected_movie_name = st.selectbox(
    'Search for a movie...',
    movies['title'].values,
    index=0
)

# ------------------ Recommend Button ------------------
if st.button('🎯 Recommend'):
    with st.spinner('Fetching top picks... 🍿'):
        recommendations = recommend(selected_movie_name)

    if recommendations:
        st.subheader('Top Recommendations:')
        for i in range(0, len(recommendations), 5):
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                if i + idx < len(recommendations):
                    movie = recommendations[i + idx]
                    col.markdown(f"""
                    <div class="movie-card">
                        <img src="{movie['poster']}" width="240">
                        <div class="movie-title">{movie['title']}</div>
                        <div class="movie-subtitle">Year: {movie['year']} | ⭐ {movie['rating']}</div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("No recommendations found!")

# ------------------ Footer ------------------
st.markdown("<div class='custom-footer'>Made with ❤️ | Powered by TMDB API & Streamlit</div>", unsafe_allow_html=True)
