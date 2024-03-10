import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import os
import io
from dotenv import load_dotenv
import pyttsx3

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


st.title("Speak & Learn: Improve Your English!")
st.write("Speak a sentence in English and click 'Check Grammar' to see if there are any potential errors.")

record_btn = st.button("Record")
recorded_text = st.empty()
grammar_result = st.empty()

input_prompt = """Assess my English response, identifying errors and offering constructive feedback in 50 words. Suggest improvements and corrections for clarity and coherence in the sentence without utilizing bullet points and do not use comma and capitalizing."""

def get_response(text,input_prompt):
    response = model.generate_content([text,input_prompt])
    return response.text

def speak(audio):
    engine = pyttsx3.init()
    engine.say(audio) 
    engine.runAndWait() 

if record_btn:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        recorded_text.text = recognizer.recognize_google(audio)
        st.session_state.text = recorded_text.text  # Store text for potential Grammarly check
        grammar_result.button("Check Grammar")
        st.write(st.session_state.text)
    except sr.UnknownValueError:
        recorded_text.text = "Could not understand audio"
    except sr.RequestError as e:
        recorded_text.text = "Could not request results from Google Speech-to-Text service; {0}".format(e)


if grammar_result and st.session_state.get("text"):
    grammar_check_result = get_response(st.session_state["text"], input_prompt)
    if grammar_check_result:
        grammar_result.text = grammar_check_result
        st.write('User: '+st.session_state.text)
        st.write(grammar_check_result)
        speak(grammar_check_result)
    else:
        grammar_result.text = "Checking grammar..."