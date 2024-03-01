from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os 
import google.generativeai as genai 

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Youtube video summarizer. You will be taking the transcript text 
and summarizing the entire video and providing the important summary in points within 250 words. 
The transcript text will be appended here: """

## Getting the transcript text
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        # `transcript_text` is a variable that stores the text transcript of the YouTube video. It is
        # extracted using the `extract_transcript_details` function, which takes the YouTube video URL
        # as input and uses the `YouTubeTranscriptApi` to retrieve the transcript text. The transcript
        # text is then stored in the `transcript_text` variable for further processing.
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " "+i["text"] 
        print("transcript="+transcript)    
        return transcript 
    except Exception as e:
        raise e  
    
## Function to load gemini pro model and get response

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt+transcript_text)
    return response.text

## Initialize streamlit app
st.set_page_config(page_title="Youtube Transcript App")
st.header('Gemini LLM Youtube Transcript Application')
input=st.text_input('Enter Youtube URL: ', key='input')
submit=st.button('Get the Summary:')

if input:
    video_id = input.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    
## When submit is clicked
if submit:
    get_transcript_text=extract_transcript_details(input)
    if get_transcript_text:
        response=generate_gemini_content(get_transcript_text, prompt)
        st.markdown('## Detailed Summary: ')
        st.write(response)

