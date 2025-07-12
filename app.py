import pickle
import streamlit as st
import requests
import os

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f1823b94760047e2bc53d5c555dec13a&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')

base_path = r'C:\Users\pags6\Downloads\Movie Recommender System\Model'

# Absolute paths to your pickle files
movie_list_path = r'C:\Users\pags6\Downloads\Movie Recommender System\Model\movie_list.pkl'
similarity_path = r'C:\Users\pags6\Downloads\Movie Recommender System\Model\similarity.pkl'

# Load pickle files
try:
    with open(movie_list_path, 'rb') as f:
        movies = pickle.load(f)

    with open(similarity_path, 'rb') as f:
        similarity = pickle.load(f)

    # Now check type of 'movies' to access titles correctly
    if isinstance(movies, list):
        # Case: movies is a list of strings (titles)
        movie_list = movies
    elif isinstance(movies, dict):
        # Case: movies is a dict with 'title' key
        movie_list = movies['title']
    else:
        try:
            # Try treating it like a DataFrame
            movie_list = movies['title'].values
        except Exception as e:
            st.error(f"Unable to extract movie titles: {e}")
            movie_list = []

    st.success("Model files loaded successfully.")
except FileNotFoundError:
    st.error("Pickle files not found. Double-check the path.")
except Exception as e:
    st.error(f"An error occurred: {e}")
#movies = pickle.load(open('model/movie_list.pkl','rb'))
#similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])