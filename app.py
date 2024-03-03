import streamlit as st
import pickle
import requests
import random


movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

header_style = """
text-align: center;
"""

# Display the centered header
st.markdown("<h1 style='text-align: center;'>🍿 RANDOMFLIX 🎬</h1>", unsafe_allow_html=True)

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

# def recommend(movie_title):
#     index = movies[movies['title'] == movies].index[0]
#     distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movies = []
#     recommended_posters = []
#     for i in distance[1:6]:
#         movie_title = movies.iloc[i[0]].title
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_posters.append(fetch_poster(movie_title))
#     return recommended_movies, recommended_posters


def recommend(movie_title):
    index = movies[movies['title'] == movie_title].index
    index = index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distance:
        movie_index = i[0]
        if movies.iloc[movie_index]['title'] != movie_title: 
            movie_title = movies.iloc[i[0]].title # Exclude the same movie
            recommended_movies.append(movies.iloc[movie_index]['title'])
            recommended_posters.append(fetch_poster(movie_title))

            if len(recommended_movies) == 5:  # Recommend top 5 similar movies
                break
    return recommended_movies, recommended_posters

# Add functionality for when the button is clicked
if st.button("Pick a Movie for Me!"):  
    selected_movie = st.empty()
    selected_movie_index = st.empty()
    selected_movie_name = st.empty()
    selected_movie_poster = st.empty()

    
    # Randomly select a movie from the list
    random_index = st.session_state.random_index = st.session_state.get('random_index', None)
    if random_index is None:
        random_index = st.session_state.random_index = random.randint(0, len(movies_list) - 1)
    selected_movie_name.text("Selected Movie: " + movies_list[random_index])
    selectvalue = movies_list[random_index]
    selectedimage = fetch_poster(selectvalue)
    if selectedimage is not None:
        st.image(selectedimage, width=250)
    else:
        st.write("No image available")
    # st.image(fetch_poster(selectvalue), width=250)

    # st.header("Similar Movies You Could Watch: ")
    # movie_name, movie_poster = recommend(selectvalue)
    # col1, col2, col3, col4, col5=st.columns(5) 
    # with col1:
    #     st.text(movie_name[0])
    #     st.image(movie_poster[0])
    # with col2:
    #     st.image(movie_poster[1])
    #     st.text(movie_name [1])
    # with col3:
    #     st.image(movie_poster[2])
    #     st.text(movie_name [2])
    # with col4:
    #     st.image(movie_poster[3])
    #     st.text(movie_name [3])
    # with col5:
    #     st.image(movie_poster[4])
    #     st.text(movie_name[4])

    st.header("Similar Movies You Could Watch: ")
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5) 
    with col1:
        if movie_poster[0] is not None:
            st.image(movie_poster[0])
        else:
            st.write("No image available")
        st.text(movie_name[0])

    with col2:
        if movie_poster[1] is not None:
            st.image(movie_poster[1])
        else:
            st.write("No image available")
        st.text(movie_name[1])

    with col3:
        if movie_poster[2] is not None:
            st.image(movie_poster[2])
        else:
            st.write("No image available")
        st.text(movie_name[2])

    with col4:
        if movie_poster[3] is not None:
            st.image(movie_poster[3])
        else:
            st.write("No image available")
        st.text(movie_name[3])

    with col5:
        if movie_poster[4] is not None:
            st.image(movie_poster[4])
        else:
            st.write("No image available")
        st.text(movie_name[4])


    # Call the recommendation model to get similar movies
    # index = movies[movies['title'] == movies_list[random_index]].index[0]
    # distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    # recommend_movie = []
    # recommend_poster = []
    # for i in distance[1:6]:
    #     movie_id = movies.iloc[i[0]]['show_id']
    #     recommend_movie.append(movies.iloc[i[0]]['title'])
    #     recommend_poster.append(fetch_poster(movie_id))
    



    
