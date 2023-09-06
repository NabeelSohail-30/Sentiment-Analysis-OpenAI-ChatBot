import json
import streamlit as st
import openai

# Streamlit app title and description
st.title("Sentiment Analysis App")
st.write("Enter a text, and we'll analyze its sentiment.")

OPENAI_API_KEY = st.sidebar.text_input("Enter your OpenAI API key:", type="password")


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "system", "content": "You are an helpful expert Sentiment Analyst that analyzes the "
                                              "sentiment and return the sentiment, sentiment score, user mood"},
                {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# Text input from the user
user_input = st.text_area("Enter your text here:")


# Function to perform sentiment analysis
def perform_sentiment_analysis(text):
    try:
        prompt = f"""
        What is the sentiment of the following text? \
        Which is delimited with triple backticks? \

        Analyze the sentiment and generate the following data in a JSON object \
        1- Sentiment (Positive or Negative) \
        2- Sentiment Score (1 to 10) \
        3- User Mood \
        
        JSON Object Example:
        {{
          "sentiment": "Positive",
          "sentiment_score": 8.5,
          "user_mood": "Happy"
        }}
        
        Text: '''{text}'''
        """

        responseJSON = get_completion(prompt)

        responseDict = json.loads(responseJSON)

        sentiment = responseDict["sentiment"]
        sentiment_score = responseDict["sentiment_score"]
        user_mood = responseDict["user_mood"]

        return sentiment, sentiment_score, user_mood
    except Exception as e:
        return str(e)


# Analyze sentiment when the user submits input
if st.button("Analyze Sentiment"):
    # Initialize the OpenAI API client
    if OPENAI_API_KEY:
        if OPENAI_API_KEY.startswith('sk-'):
            openai.api_key = OPENAI_API_KEY

            if user_input:
                sentiment, sentiment_score, user_mood = perform_sentiment_analysis(user_input)
                st.write(f"Sentiment: {sentiment}")
                st.write(f"Sentiment Score: {sentiment_score}")
                st.write(f"User Mood: {user_mood}")
            else:
                st.warning("Please enter some text to analyze.")
        else:
            st.sidebar.warning("Invalid API Key")
    else:
        st.sidebar.warning("API Key Not Found, Enter API Key to continue")
