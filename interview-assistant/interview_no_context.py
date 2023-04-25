import openai
import speech_recognition as sr
import pyttsx3

# Set up OpenAI API
openai.api_key = "YOUR-API_KEY_HERE"
model_engine = "text-davinci-002"

# Set up text-to-speech engine with Microsoft David voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use the Microsoft David voice

# Get the first question from OpenAI API
first_prompt = """act as an expert IT recruiter with extended knowledge of [JAVA]. Ask me questions one by one to simulate an interview. DO NOT GIVE THE ANSWER.
    When I type answer, just provide the right answer in the first person as an expert, who is extremely competent about that topic.
    Do not repeat the same questions in this chat.
    Proceed with just one question at a time and wait for my answer."""

# Ask the user to start the interview
engine.say("Welcome to the Java Interview. Please wait for the first question.")
engine.runAndWait()

# Ask the first question to the user and wait for response
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Please speak your first question.")
    audio = r.listen(source)

try:
    user_input = r.recognize_google(audio)
    print("User: ", user_input)

    response = openai.Completion.create(
        engine=model_engine,
        prompt=user_input,
        max_tokens=1024,
        n=1,
        stop= "n",
        temperature=0.2,
    )

    # Convert chatbot response to speech
    bot_response = response.choices[0].text
    print("Bot: ", bot_response)
    engine.say(bot_response)
    engine.runAndWait()

    # Log the conversation to console
    print("Question: ", user_input)
    print("Answer: ", bot_response)

    # Ask the user if they want to continue or stop
    engine.say("Do you want to continue? Say next or no.")
    engine.runAndWait()

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Do you want to continue? Say NEXT or NO.")
        audio = r.listen(source)

    try:
        user_input = r.recognize_google(audio)
        print("User: ", user_input)
        if user_input.upper() == "NO":
            engine.say("Thank you for participating in the Java Interview. Goodbye!")
            engine.runAndWait()
            exit()
        elif user_input == "next":
            response = openai.Completion.create(
                engine=model_engine,
                prompt=first_prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            first_question = response.choices[0].text
            engine.say(first_question)
            engine.runAndWait()

    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError:
        print("Sorry, my speech recognition service is down.")

except sr.UnknownValueError:
    print("Sorry, I didn't understand that.")
except sr.RequestError:
    print("Sorry, my speech recognition service is down.")
