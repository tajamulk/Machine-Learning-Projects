import pickle
import streamlit as st
import requests
from PIL import Image

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    recommended_indices = distances.argsort()[::-1][1:6]
    recommended_movie_names = movies.iloc[recommended_indices]['title'].values
    recommended_movie_posters = [fetch_poster(movies.iloc[i]['movie_id']) for i in recommended_indices]
    recommended_movie_overviews = movies.iloc[recommended_indices]['overview'].values
    return recommended_movie_names, recommended_movie_posters, recommended_movie_overviews

st.set_page_config(page_title="Movie Recommender System", page_icon=":movie_camera:", layout="wide")

# Set background color and font size for the entire app
st.markdown("""
    <style>
        body {
            background-color: #F5F5F5;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Add a banner at the top of the page
image = Image.open("Movie-Recommendation2.jpeg")
st.image(image, use_column_width=True)

# Add a title and a description
st.title("Movie Recommender System")
st.write("""
    This app recommends similar movies based on the user's selection. It uses a content-based recommendation
    system that recommends movies with similar plot summaries.
""")

# Load the list of movies and similarity matrix from the pickle files
movies = pickle.load(open('file1.pkl', 'rb'))
similarity = pickle.load(open('file2.pkl', 'rb'))

# Add a dropdown to select a movie
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values,
    key="movie-dropdown"
)

# Add a button to trigger the recommendation
if st.button('Show Recommendation'):
    # Add a title for the recommended movies
    st.subheader("You may also like:")
    recommended_movie_names, recommended_movie_posters, recommended_movie_overviews = recommend(selected_movie)

    # Divide the page into 5 columns to show the recommended movies
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    # Add a title for the recommended movies
    st.write('''Thank you for visiting our Movie Recommender System! We hope you enjoyed using it.
             If you have a moment, we would appreciate your feedback in the LinkedIn comment section.
             Thank you!''')

    # Loop through the columns and add the recommended movies
    for i, col in enumerate(cols):
        with col:
            st.subheader(recommended_movie_names[i])
            st.image(recommended_movie_posters[i], use_column_width=True)
            st.write(recommended_movie_overviews[i])
