# Email Check/Summary and Voice Interaction with Llama 3

This project is a Python application that reads unread emails from Gmail, summarizes them using an LLM (Llama 3), and allows the user to interact with the model via voice commands. The user can ask questions, and the LLM will respond audibly. The conversation continues until the user decides to stop.

## Features
- Fetches unread emails from Gmail.
- Summarizes the emails using the Llama 3 model.
- Interacts with the user through voice commands.
- Continuous conversation with the LLM until the user ends it.
- Text-to-speech (TTS) and Speech-to-text (STT) using `pyttsx3` and `speech_recognition`.

## Requirements

- Python 3.12
- [SimpleGmail](https://github.com/jeremyephron/simplegmail) (for fetching Gmail messages)
- [Pyttsx3](https://pyttsx3.readthedocs.io/en/latest/) (for text-to-speech)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) (for speech-to-text)
- [Requests](https://pypi.org/project/requests/) (for making HTTP requests to the Llama model)
- PyAudio
  
## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/andyanalog/email-checkTTS-STT.git
    cd email-checkTTS-STT
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use: env\Scripts\activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the `simplegmail` library:
    - Follow the [SimpleGmail guide](https://github.com/jeremyephron/simplegmail) to authenticate and allow access to your Gmail account.

5. Run the application:
    ```bash
    python read_emails_stt.py
    ```

## Usage

- The application will fetch unread emails from your Gmail inbox and summarize them using the Llama model.
- The email summary will be spoken aloud to you.
- You will be asked if you'd like to know anything else. Respond with "yes" to ask follow-up questions, or "no" to end the conversation.
- You can continue asking questions in a conversational manner until you choose to stop.

## Notes

- Ensure that the Llama 3 model is running locally and available at `http://localhost:11434/api/generate`.
- The application uses the `speech_recognition` library to listen to your voice, so ensure your microphone is properly configured.
- To prevent uploading unnecessary files like virtual environments, add them to `.gitignore`.

## Contributing

Feel free to open issues or submit pull requests if you'd like to contribute to the project.

## License

This project is licensed under the MIT License. See the [MIT LICENSE](LICENSE) file for more details.
