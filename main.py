import streamlit as st
import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import requests
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import main_functions


api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]

st.title("COP 4813 - Web Application Programming")
st.title("Project 1")
st.header("Part A - The Stories API")

st.write("This app uses the Top Stories API to display the most common words used in the top current")
st.write(" articles based on a specific topic selected by the user. The data is displayed as a line")
st.write(" chart and as a wordcloud image.")

st.subheader("I- Topic Selection")

name = st.text_input("Please enter your name")

options = st.selectbox("Select a topic of your interest",
                       ["", "Arts", "Automobiles", "Books", "Business", "Fashion",
                        "Food", "Health", "Home", "Insider", "Magazine", "Movies",
                        "NYRegion", "Obituaries", "Opinion", "Politics", "RealEstate",
                        "Science", "Sports", "SundayReview", "Technology", "Theater",
                        "T-Magazine", "Travel", "Upshot", "US", "World"])

if options and name:
    st.write("Hi {},".format(name) + " you selected the {}".format(options) + " topic")

    url = "https://api.nytimes.com/svc/topstories/v2/" + options + ".json?api-key=" + api_key

    response = requests.get(url).json()

    main_functions.save_to_file(response, "JSON_Files/response.json")

    my_articles = main_functions.read_from_file("JSON_Files/response.json")

    str1 = ""
    for i in my_articles["results"]:
        str1 = str1 + i["abstract"]

    words = word_tokenize(str1)

    fdist = FreqDist(words)

    words_no_punc = []

    for w in words:
        if w.isalpha():
            words_no_punc.append(w.lower())

    fdist1 = FreqDist(words_no_punc)

    sw = stopwords.words("english")

    clean_words = []

    for w in words_no_punc:
        if w not in sw:
            clean_words.append(w)

    fdist2 = FreqDist(clean_words)

    fnl = fdist2.most_common(10)

    st.subheader("II - Frequency Distribution")
    selection = st.checkbox("Click here to generate frequency distribution")

    if selection:
        most_common = pd.DataFrame(fnl)
        df = pd.DataFrame({"words": most_common[0], "count": most_common[1]})
        import plotly.express as px

        fig = px.line(df, x="words", y="count", title='')
        st.plotly_chart(fig)

    st.subheader("III - Wordcloud")
    selection = st.checkbox("Click here to generate Wordcloud")

    if selection:

        wordcloud = WordCloud().generate(str1)

        plt.figure(figsize=(12, 12))
        plt.imshow(wordcloud, interpolation='bilinear')

        plt.axis("off")
        plt.show()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

# PART B

st.header("Part B - Most Popular Articles")
st.write("Select if you want to see the most shared, emailed or viewed articles.")

options2 = st.selectbox("Select your preferred set of articles",
                        ["", "shared", "emailed", "viewed"])

options3 = st.selectbox("Select the period of time (last days)",
                        ["", "1", "7", "30"])

if options2 and options3:

    url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + options2 + "/" + options3 + ".json?api-key=" + api_key

    response2 = requests.get(url2).json()

    main_functions.save_to_file(response2, "JSON_Files/response2.json")
    my_articles2 = main_functions.read_from_file("JSON_Files/response2.json")

    str2 = ""
    for i in my_articles2["results"]:
        str2 = str2 + i["abstract"]

    words2 = word_tokenize(str2)

    fdist3 = FreqDist(words2)

    words_no_punc2 = []

    for w in words2:
        if w.isalpha():
            words_no_punc2.append(w.lower())

    fdist4 = FreqDist(words_no_punc2)

    sw2 = stopwords.words("english")

    clean_words2 = []

    for w in words_no_punc2:
        if w not in sw2:
            clean_words2.append(w)

    fdist5 = FreqDist(clean_words2)

    wordcloud2 = WordCloud().generate(str2)

    plt.figure(figsize=(12, 12))
    plt.imshow(wordcloud2, interpolation='bilinear')

    plt.axis("off")
    plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
