from simplegmail import Gmail
from simplegmail.query import construct_query
import requests
import pyttsx3
import speech_recognition as sr
import re

# Function to clean LLM's response
def clean_llm_response(response):
    """
    Cleans the LLM's response by removing unwanted symbols, repetitive phrases, or patterns.
    """
    # Remove any asterisks, extra symbols, or unwanted words.
    cleaned_response = re.sub(r"[^\w\s.,!?]", "", response)  # Remove non-alphanumeric except punctuation
    
    # Optionally, remove specific phrases like "astheric" if they appear frequently
    cleaned_response = cleaned_response.replace("astheric", "")

    # Remove any leading or trailing spaces
    cleaned_response = cleaned_response.strip()

    return cleaned_response


# Function to initialize pyttsx3 and read the text
def speak_text(text):
    engine = pyttsx3.init()

    # Adjust voice properties
    engine.setProperty('rate', 150)  # Speed of the voice
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

    # Get available voices information
    voices = engine.getProperty('voices')
    #for voice in voices:
    #    print(f"Voice: {voice.name}, ID: {voice.id}, Languages: {voice.languages}")

    # Speak the text
    engine.say(text)
    engine.runAndWait()

# Function to convert speech to text using the SpeechRecognition library
def listen_to_voice():
    recognizer = sr.Recognizer()

    # Use the microphone as the audio input source
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

    # Attempt to recognize the audio
    try:
        response_text = recognizer.recognize_google(audio, language="en-US")  # Using English
        print(f"User said: {response_text}")
        return response_text
    except sr.UnknownValueError:
        print("Could not understand what you said.")
        return None
    except sr.RequestError:
        print("Error connecting to the speech recognition service.")
        return None

# Initialize Gmail
gmail = Gmail()

# Define query parameters to fetch unread emails
query_params = {
    "newer_than": (1, "day"),
    "unread": True,
    "category": "primary",
}

# Get unread messages
messages = gmail.get_unread_inbox(query=construct_query(query_params))

# Prepare a summary of the emails
email_summary = ""

for message in messages:
    email_summary += f"From: {message.sender}\n"
    email_summary += f"Subject: {message.subject}\n"
    email_summary += f"Date: {message.date}\n"
    email_summary += f"Preview: {message.snippet}\n\n"

# Check if there are unread emails to send to the model
if email_summary:
    # Define the payload for the model
    payload = {
        "model": "llama3:latest",
        "stream": False,
        "prompt": f"Give me a summary of the following emails. You can enumerate them but do not use any symbols in the summary:\n\n{email_summary}",
    }

    # Make the request to the Llama server
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            headers={'Content-Type': 'application/json'},
            json=payload
        )

        # Raise an error if the request was not successful
        response.raise_for_status()

        # Convert the response to JSON
        result = response.json()

        # Access only the relevant content for the summary
        summary = result.get('response', 'No summary generated.')
        print("Summary of unread emails:", summary)

        # Call the function to read the summary aloud
        speak_text(summary)

        while True:  # Start a loop for continuous conversation
            # Ask if the user wants to know anything else
            speak_text("Would you like to know something else?")
            user_response = listen_to_voice()

            if user_response:
                if "yes" in user_response.lower():
                    speak_text("Please ask your question.")
                    # Listen for the user's query to send to the LLM
                    user_question = listen_to_voice()

                    if user_question:
                        # Define the payload for the user's question
                        question_payload = {
                            "model": "llama3:latest",
                            "stream": False,
                            "prompt": f"{user_question}",
                        }

                        # Make the request to the Llama server for the user's question
                        try:
                            question_response = requests.post(
                                'http://localhost:11434/api/generate',
                                headers={'Content-Type': 'application/json'},
                                json=question_payload
                            )

                            # Raise an error if the request was not successful
                            question_response.raise_for_status()

                            # Convert the response to JSON
                            question_result = question_response.json()

                            # Access only the relevant content for the response
                            question_answer = question_result.get('response', 'No answer generated.')

                            cleaned_response = clean_llm_response(question_answer)

                            print("Answer to your question:", question_answer)

                            # Read the answer aloud
                            speak_text(question_answer)

                        except requests.exceptions.RequestException as e:
                            print(f"Error communicating with llama model: {e}")
                        except ValueError as e:
                            print(f"Error parsing the response: {e}")

                elif "no" in user_response.lower():
                    speak_text("Okay, ending the conversation now.")
                    break  # Exit the loop if the user says "no"
                else:
                    speak_text("I didn't catch that. Please respond with 'yes' or 'no'.")
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with llama model: {e}")
    except ValueError as e:
        print(f"Error parsing the response: {e}")
else:
    print("No new unread emails to summarize.")
