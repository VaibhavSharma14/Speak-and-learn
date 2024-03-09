'''import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("Speak & Learn: Improve Your English!")
st.write("Speak a sentence in English and click 'Check Grammar' to see if there are any potential errors.")

record_btn = st.button("Record")
recorded_text = st.empty()
grammar_result = st.empty()

model = genai.GenerativeModel('gemini-pro')


input_prompt = """please evaluate my grammatical mistakes and give me suggestions how to improve it in 100 words only """

def get_response(text,input_prompt):
    response = model.generate_content([text,input_prompt])
    return response.text

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
  grammar_check_result = get_response(st.session_state["text"],input_prompt)
  if grammar_check_result:
    grammar_result.text = grammar_check_result
    tts = gTTS(grammar_check_result, lang='en')
    tts.save('output_audio.mp3')
  else:
    grammar_result.text = "Checking grammar..."

    
if os.path.exists('output_audio.mp3'):
    audio = AudioSegment.from_mp3('output_audio.mp3')
    play(audio)
else:
    st.warning("No audio file found.")'''
    
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

engine = pyttsx3.init() 


st.title("Speak & Learn: Improve Your English!")
st.write("Speak a sentence in English and click 'Check Grammar' to see if there are any potential errors.")

record_btn = st.button("Record")
recorded_text = st.empty()
grammar_result = st.empty()

input_prompt = """Assess my English response, identifying errors and offering constructive feedback in 50 words. Suggest improvements and corrections for clarity and coherence in the sentence without utilizing bullet points. Provide guidance on how to enhance overall speaking proficiency and refine the targeted sentence for better articulation."""
def get_response(text,input_prompt):
    response = model.generate_content([text,input_prompt])
    return response.text

def speak(audio):
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
        st.write(grammar_check_result)
        speak(grammar_check_result)
    else:
        grammar_result.text = "Checking grammar..."


        


