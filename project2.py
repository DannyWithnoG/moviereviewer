import streamlit as st
import requests
import pandas as pd
import datetime

API_KEY = "51a2790ee65ff89d9389903710a4b099"
BASE_URL = "https://api.themoviedb.org/3"

st.set_page_config(page_title="Movie Reviewer", page_icon="movie icon.png")

def search_movie(query):
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}"
    response = requests.get(url)
    return response.json().get("results", [])


def get_trending():
    url = f"{BASE_URL}/trending/movie/week?api_key={API_KEY}"
    response = requests.get(url)
    return response.json().get("results", [])


def upcoming_released():
    today = datetime.date.today().strftime('%Y-%m-%d')
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&primary_release_date.gte={today}&sort_by=release_date.asc"
    response = requests.get(url)
    return response.json().get("results", [])


def get_genres(genre_ids):
    genre_dict = {
        28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
        80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
        14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
        9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
        10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
    }
    return [genre_dict.get(genre_id, "Unknown") for genre_id in genre_ids]


st.title("Movie Reviewer")

tabs = st.tabs(["Home", "Search for Movies", "Trending Movies", "Upcoming Releases", "Exit"])

with tabs[0]:
    st.subheader("Welcome to the Movie Reviewer Website!")
    st.write("Explore trending movies, search for your favorites, and view upcoming releases.")

with tabs[1]:
    query = st.text_input("Enter a movie name:")
    if st.button("Search"):
        if query:
            results = search_movie(query)
            if results:
                for movie in results[:5]:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if movie.get("poster_path"):
                            st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}", width=200)
                    with col2:
                        st.subheader(movie["title"])
                        st.write(f"**Release Date:** {movie['release_date']}")
                        st.write(f"**Rating:** {movie['vote_average']}/10")
                        st.write(f"**Overview:** {movie['overview']}")
            else:
                st.warning("No results found.")
        else:
            st.info("Please enter a movie name.")

with tabs[2]:
    st.subheader("Trending Movies")
    trending_movies = get_trending()

    if trending_movies:
        df = pd.DataFrame(trending_movies, columns=["title", "release_date", "vote_average", "genre_ids"])
        df = df.rename(columns={"title": "Movie", "release_date": "Release Date", "vote_average": "Rating"})

        df["Genre"] = df["genre_ids"].apply(get_genres)
        df = df.drop(columns=["genre_ids"])

        sort_by = st.selectbox("Sort by:", ["Movie", "Release Date", "Rating"], key="trending_sort_by")
        sort_order = st.selectbox("Sort order:", ["Ascending", "Descending"], key="trending_sort_order")

        if sort_by == "Movie":
            df = df.sort_values(by="Movie", ascending=(sort_order == "Ascending"))
        elif sort_by == "Release Date":
            df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")
            df = df.sort_values(by="Release Date", ascending=(sort_order == "Ascending"))
        elif sort_by == "Rating":
            df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
            df = df.sort_values(by="Rating", ascending=(sort_order == "Ascending"))

        max_title_length = df['Movie'].apply(len).max()
        width = max(300, max_title_length * 7)

        styled_df = df.style.set_properties(subset=["Movie"], **{"width": f"{width}px"})

        st.dataframe(styled_df)
    else:
        st.error("Failed to fetch trending movies.")

with tabs[3]:
    st.subheader("Upcoming Releases")
    upcoming_movies = upcoming_released()

    if upcoming_movies:
        df = pd.DataFrame(upcoming_movies, columns=["title", "release_date", "vote_average", "genre_ids"])
        df = df.rename(columns={"title": "Movie", "release_date": "Release Date", "vote_average": "Rating"})

        df["Genre"] = df["genre_ids"].apply(get_genres)
        df = df.drop(columns=["genre_ids", "Rating"])

        sort_by = st.selectbox("Sort by:", ["Movie", "Release Date"], key="upcoming_releases_sort_by")
        sort_order = st.selectbox("Sort order:", ["Ascending", "Descending"], key="upcoming_releases_sort_order")

        if sort_by == "Movie":
            df = df.sort_values(by="Movie", ascending=(sort_order == "Ascending"))
        elif sort_by == "Release Date":
            df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")
            df = df.sort_values(by="Release Date", ascending=(sort_order == "Ascending"))

        max_title_length = df['Movie'].apply(len).max()
        width = max(300, max_title_length * 7)

        styled_df = df.style.set_properties(subset=["Movie"], **{"width": f"{width}px"})

        st.dataframe(styled_df)
    else:
        st.error("Failed to fetch upcoming movies.")

with tabs[4]:
    st.subheader("Thank you for using the Movie Reviewer website!")
    st.write("I hope you found the information helpful. Feel free to exit now.")