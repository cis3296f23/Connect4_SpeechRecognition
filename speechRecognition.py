import speech_recognition as sr

num_dict = {
    'one': '1',
    'two': '2',
    'to': '2',
    'three': '3',
    'four': '4',
    'for': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
}
COLUMN_COUNT = 7
class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def get_speech_input(self):
        with self.microphone as source:
            print("Say the column number to drop the chip:")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)

        try:
            spoken_text = self.recognizer.recognize_google(audio).lower()
            print(spoken_text)
            return spoken_text
        except sr.UnknownValueError:
            print("Sorry, I did not understand. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    def speech_recognition_move(self, gl, board):
        spoken_text = self.get_speech_input()
        if spoken_text is not None:
            try:
                numbers = [word for word in spoken_text.split() if word.lower() in num_dict]
                print(numbers)
                column = int(''.join(num_dict[word.lower()] for word in numbers))
                print(column)
                if 1 <= column <= COLUMN_COUNT and gl.is_valid_location(board, column - 1):
                    return column - 1
                else:
                    print("Invalid column number. Please try again.")
                    return None
            except ValueError:
                print("Invalid input. Please say a valid column number.")
                return None

        return None