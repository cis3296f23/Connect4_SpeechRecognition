import speech_recognition as sr

class SpeechRecognitionHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize_speech(self):
        with sr.Microphone() as source:
            print("Say something:")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()  # Convert to lowercase for case-insensitive comparisons
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

# Example usage:
# speech_recognition_handler = SpeechRecognitionHandler()
# user_input = speech_recognition_handler.recognize_speech()
