import speech_recognition as sr
import openai
from googletrans import Translator
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup
import tempfile
import os
from gtts import gTTS


def listen_activation_phrase():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Waiting for the activation phrase...")
            audio_data = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio_data, language='en-EN')
                if "jarvis" in text.lower():
                    text_to_speech("Yes, sir. How may I assist you?")
                    return
            except sr.UnknownValueError:
                pass


def listen_question():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data, language='en-EN')
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat your question?")
            return listen_question()

def get_gpt_context(context):
    openai.api_key = "YOUR-APIKEY-HERE"
    resultCtx = openai.Completion.create(
        engine="text-davinci-002",
        prompt= f" Summarize this chat and create a breif short description about context, max 100 token : {context}.",
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.0,
        top_p=1
    )
    response = resultCtx.choices[0].text.strip()
    return response
    
def get_gpt_response(context , question):
    openai.api_key = "YOUR-APIKEY-HERE"
    result = openai.Completion.create(
        engine="text-davinci-002",
        prompt= f" Act as an expert of this following topic and give me an answer about: {question}. considering we are talking about context: {context}. summarize it to not exceed token limit",
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.8,
        top_p=1
    )
    response = result.choices[0].text.strip()
    return response


def text_to_speech(text, speed_factor=1.2):
    tts = gTTS(text, lang='en')

    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        temp_filename = temp_audio_file.name
        tts.save(temp_filename)

    audio = AudioSegment.from_file(temp_filename, format="mp3")
    audio = speedup(audio, speed_factor)
    play(audio)
    os.remove(temp_filename)


def main():
    context = " no context "
    while True:
        listen_activation_phrase()
        question = listen_question()
        if question:
            print("OLD context:", context)
            print("QUESTION:", question)
            response = get_gpt_response(context, question)
            print("ANSWER:",response)
            context = get_gpt_context(response)
            print("NEW context:", context)
            text_to_speech(response)

        else:
            print("Sorry, I didn't catch that. Could you please repeat your question?")
        
        print("Do you have any more questions? ")
        

if __name__ == "__main__":
    main()

