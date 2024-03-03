import streamlit as st
import pickle
import requests
import random


movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# HTML/CSS/JavaScript code for spinning wheel
html_code = """
<style>
/* CSS for spinning wheel animation */
.spinner {
  width: 300px;
  height: 300px;
  position: relative;
}

.segment {
  position: absolute;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 150px 75px 0;
  border-color: #007bff transparent transparent transparent;
  transform-origin: 50% 100%;
}

.segment:nth-child(1) {
  transform: rotate(0deg);
}
.segment:nth-child(2) {
  transform: rotate(60deg);
}
.segment:nth-child(3) {
  transform: rotate(120deg);
}
.segment:nth-child(4) {
  transform: rotate(180deg);
}
.segment:nth-child(5) {
  transform: rotate(240deg);
}
.segment:nth-child(6) {
  transform: rotate(300deg);
}

.movie-name {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 20px;
  font-weight: bold;
  color: white;
}
</style>

<!-- HTML for spinning wheel -->
<div class="spinner">
  <div class="segment"></div>
  <div class="segment"></div>
  <div class="segment"></div>
  <div class="segment"></div>
  <div class="segment"></div>
  <div class="segment"></div>
</div>

<script>
function rotateWheel() {
  var spinner = document.querySelector('.spinner');
  var rotation = 0;
  var intervalId = setInterval(function() {
    rotation += 15; // Increase the rotation angle by 15 degrees
    spinner.style.transform = 'rotate(' + rotation + 'deg)';
  }, 100); // Adjust the interval duration for the speed of rotation

  // Stop the rotation after 3 seconds
  setTimeout(function() {
    clearInterval(intervalId);
  }, 3000); // Adjust the duration of rotation
}
</script>
"""


st.markdown(html_code, unsafe_allow_html=True)
st.header("Movie Recommender System")

# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=1c827bec84375d8eab8f7bd655d17749".format(movie_id)
#     data=requests.get(url)
#     data=data.json()
#     print(data)
#     poster_path = data["poster_path"]
#     full_path = "https://image.tmdb.org/t/p/w500"+poster_path
#     return full_path

def fetch_poster(movie_name):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "query": movie_name,
        "api_key": "1c827bec84375d8eab8f7bd655d17749"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'results' in data and len(data['results']) > 0:
        # Assuming the first result is the desired movie
        movie_info = data['results'][0]
        poster_path = movie_info.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500" + poster_path
            return full_path
    return None  

def recommend(movie_title):
    index = movies[movies['title'] == movies].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distance[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_title))
    return recommended_movies, recommended_posters

if st.button("Spin the Wheel"):
    rotateWheel()
    selected_movie = st.empty()
    selected_movie_index = st.empty()
    selected_movie_index.text("Selected Movie Index:")
    selected_movie_name = st.empty()
    selected_movie_poster = st.empty()

    
    # Randomly select a movie from the list
    random_index = st.session_state.random_index = st.session_state.get('random_index', None)
    if random_index is None:
        random_index = st.session_state.random_index = random.randint(0, len(movies_list) - 1)
    # selected_movie_index.text("Selected Movie Index: " + str(random_index))
    selected_movie_name.text("Selected Movie: " + movies_list[random_index])
    selectvalue = movies_list[random_index]

    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5=st.columns(5) 
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name [1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name [2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name [3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])

    # Call the recommendation model to get similar movies
    # index = movies[movies['title'] == movies_list[random_index]].index[0]
    # distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    # recommend_movie = []
    # recommend_poster = []
    # for i in distance[1:6]:
    #     movie_id = movies.iloc[i[0]]['show_id']
    #     recommend_movie.append(movies.iloc[i[0]]['title'])
    #     recommend_poster.append(fetch_poster(movie_id))
    



    
