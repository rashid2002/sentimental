import streamlit as st
from textblob import TextBlob
import emoji
import matplotlib.pyplot as plt
import requests
import pandas as pd

# Set page config as the very first Streamlit command
st.set_page_config(page_title="Movie Sentiment Analysis", layout="wide")

apiKey = 'c83aac3a811889a413c78c456a4c85b2'
baseURL = 'https://api.themoviedb.org/3'

def getMovies(movieName):
    query_params = {
        'api_key': apiKey,
        'language': 'en-US',
        'query': movieName,
        'page': 1,
        'include_adult': False
    }
    response = requests.get(f'{baseURL}/search/movie', params=query_params, timeout=10)
    return response.json().get('results', [])

def displayMovieContent(movie, ax, index, movies, sentiments):
    title = f"{movie['title']} ({movie.get('release_date', 'Unknown year')})"
    description = movie.get('overview', 'No description available.')
    sentiment_score = TextBlob(description).sentiment.polarity
    emoji_icon = emoji.emojize(':smiling_face:') if sentiment_score > 0 else emoji.emojize(':disappointed_face:')
    
    sentiments.append(sentiment_score)
    
    # Display details
    st.write(f"**{title}**")
    st.write(f"**Rating:** {movie.get('vote_average', 'N/A')} ⭐")
    st.write(f"**Description:** {description}")
    st.write(f"**Sentiment:** {emoji_icon} {sentiment_score:.2f}")

    # Update plot with sentiment data
    ax.barh(index, sentiment_score, color='skyblue', edgecolor='black')
    ax.set_yticks(range(len(movies)))
    ax.set_yticklabels([m['title'] for m in movies], fontsize=12)
    ax.set_xlabel("Sentiment Polarity", fontsize=14)
    ax.text(sentiment_score, index, f' {emoji_icon} {sentiment_score:.2f}', va='center', fontsize=12)

def renderPage():
    st.title("Sentiment Analysis on Movie Descriptions")
    
    st.subheader("TMDb Movie Description Analysis")
    movieName = st.text_input('Movie Name', placeholder='Enter movie name here...')
    
    if st.button('Search'):
        if movieName:
            movies = getMovies(movieName)
            if movies:
                sentiments = []
                st.subheader("Search Results")
                fig, ax = plt.subplots(figsize=(10, len(movies) * 0.5))
                for index, movie in enumerate(movies):
                    displayMovieContent(movie, ax, index, movies, sentiments)
                st.pyplot(fig)
                
                # Pie chart for sentiment analysis
                positive_count = sum(1 for s in sentiments if s > 0)
                negative_count = len(sentiments) - positive_count
                labels = ['Positive', 'Negative']
                sizes = [positive_count, negative_count]
                explode = (0.1, 0)  # explode 1st slice
                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(fig1)

            else:
                st.error("No movies found for the given search query.")
        else:
            st.warning("Please enter a movie name.")

if __name__ == "__main__":
    renderPage()
