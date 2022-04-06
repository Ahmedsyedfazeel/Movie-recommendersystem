import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Movie Recommender System')

movies_list = pickle.load(open('Movies_dict.pkl','rb'))
similarity = pickle.load(open('Similarity.pkl','rb'))
movies = pd.DataFrame(movies_list)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9048fd1a0c81adbf1110f13ecddb430e&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w185/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

selected_movie_name = st.selectbox('Which movie you want to watch? i will recommend you to watch similar movies', movies['title'].values)

if st.button('Recommend'):
    name, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(posters[0])

    with col2:
        st.text(name[1])
        st.image(posters[1])

    with col3:
        st.text(name[2])
        st.image(posters[2])

    with col4:
        st.text(name[3])
        st.image(posters[3])

    with col5:
        st.text(name[4])
        st.image(posters[4])

