import speech_recognition as sr
import openai
from googletrans import Translator
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup
import tempfile
import os
from gtts import gTTS


def listen_question():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ascoltando...")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data, language='en-EN')
            return text
        except sr.UnknownValueError:
            print("Non ho capito, ripeti per favore.")
            return listen_question()


def get_gpt_response(prompt):
    openai.api_key = "YOUR-APIKEY-HERE"
    result = openai.Completion.create(
        engine="text-davinci-002",
        prompt= "act as an expert in IT, Please provide a detailed and comprehensive explanation of the topic:"+ prompt +" - with some examples",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.8,
        top_p=1
    )
    response = result.choices[0].text.strip()
    return response


def text_to_speech(text, speed_factor=1.3):
    tts = gTTS(text, lang='en')

    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        temp_filename = temp_audio_file.name
        tts.save(temp_filename)

    audio = AudioSegment.from_file(temp_filename, format="mp3")
    audio = speedup(audio, speed_factor)
    play(audio)
    os.remove(temp_filename)

def main():
    while True:
        question = listen_question()
        if question:
            print("Hai chiesto:", question)
            prompt = f"Answer this technical coding question concisely and precisely: {question}"
            response = get_gpt_response(prompt)
            print("Risposta:", response)
            text_to_speech(response)
        else:
            print("Non ho capito, ripeti per favore.")
        
        print("Vuoi continuare? (y/n)")
        user_input = input()
        if user_input.lower() == 'n':
            break


if __name__ == "__main__":
    main()

