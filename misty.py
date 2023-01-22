from speech_dict import script1_dict, script2_dict, script3_dict

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import speech_recognition as sr
import base64
import time
import threading

class MistyRobot():
    def __init__(self, ip: str) -> None:
        """init MistyRobot

        Args:
            ip: IP address of Misty
        """        
        self.misty = Robot(ip)

        self.face_recognition_event = self.misty.register_event('FaceRecognition', Events.FaceRecognition, keep_alive=True)

        self.last_text_to_speech = None
        self.last_voice_record = None

        self.known_faces = self.misty.get_known_faces().json()['result']
        self.present_patients = []

        self.misty.display_image('e_Sleeping.jpg')
        self.misty.change_led(196, 160, 0)
        self.misty.move_head(0, 0, 0, velocity=80, units='position')
        time.sleep(3)

        print(self.known_faces)

    def wait_for_face(self) -> str:
        """Wait until a face appears in Misty's field of view.

        Returns:
            Name of recognized face, 'unknown person' is returned if face is unrecognized.
        """
        while True:
            data = self.face_recognition_event.data
            print(data)
            # Event data of signal containing succesful face detection does not contain 'status' key.
            if 'status' not in data:
                # Open Misty's eyes.
                self.misty.display_image('e_DefaultContent.jpg')
                # Change LED color to green.
                self.misty.change_led(78, 154, 6)

                return data['message']['personName']

    def track_face(self) -> None:
        """Keep Misty's face oriented at the person in front of her.
        """        
        yaw = 0
        pitch = 0

        while True:
            try:
                detected_face = self.face_recognition_event.data['message']
                bearing = detected_face['bearing'] # x-axis (yaw)
                elevation = detected_face['elevation'] # y-axis (pitch)

                new_yaw = yaw + 0.2 * bearing
                new_pitch = pitch + 0.2 * elevation

                # Boundaries.
                if new_yaw < 5 and new_pitch < 5:

                    self.misty.move_head(new_pitch, 0, new_yaw, velocity=90, units='position')

                    yaw = new_yaw
                    pitch = new_pitch

                    time.sleep(2)
            except:
                print('no face and cum')

    def train_face(self, name: str) -> None:
        """Train a new face in front of Misty andd give it a name.

        Args:
            name: Name given to face.
        """        
        self.misty.speak("Please look at me until I am done learning your face.")
        time.sleep(5)

        face_training_event = self.misty.register_event(Events.FaceTraining, 'FaceTraining', keep_alive=True)
        self.misty.start_face_training(name)

        while True:
            data = face_training_event.data
            
            # If face training is complete, 'isProcessComplete' equals True
            if data['message']['isProcessComplete']:
                self.misty.unregister_event('FaceTraining')
                break

        self.misty.speak("I have succesfully learned your face.")
        time.sleep(4)
        
    def greet(self, name: str) -> None:
        """Choose what script to execute based on recognition of face and if the patient is coming or leaving.

        Args:
            name: Patient name.
        """        
        if name in self.known_faces:
            if name in self.present_patients:
                self.start_script3(name)
                self.present_patients.remove(name)
            else:
                self.start_script1(name)
                self.present_patients.append(name)
        else:
            name = self.start_script2()
            self.present_patients.append(name)

    def start_script1(self, name = 'Lucas', formality: str = 'informal'):
        """Start conversation according to script 1.

        Args:
            formality: Formality of conversation. Defaults to 'informal'.
        """        
        speech_dict = script1_dict
        print('script1')
        for entry, question in speech_dict.items():
            print(entry)
            if entry == 'check_appointment_unknown':
                self.ask(question[formality])

            elif entry == 'ask_face_scan':
                # self.train_face(name)
                ...
            elif entry in ['confirm_appointment_unknown', 'prompt_health_form', 'finish_intake'] and formality == 'informal':
                self.ask(str(question[formality].format(name)))
            else:
                print(entry)
                print(question[formality])
                self.ask(question[formality])

    def ask(self, question: str) -> str:
        """Let Misty ask a question and procecss the audio response to text.

        Args:
            question: Question asked by Misty.

        Returns:
            Text response given.
        """        
        self.misty.speak(question, utteranceId=question)
        print('skeer')
        text_to_speech_complete_event = self.misty.register_event(Events.TextToSpeechComplete, 'TextToSpeechComplete', keep_alive=True)
        while True:
            data = text_to_speech_complete_event.data
            # Event data of signal containing succesful speech completion does not contain 'status' key.
            if 'status' not in data:
                self.misty.unregister_event('TextToSpeechComplete')
                break
        
        voice_record_event = self.misty.register_event(Events.VoiceRecord, 'VoiceRecord', keep_alive=True)
        self.misty.capture_speech(overwriteExisting=True, maxSpeechLength=15000)
        while True:
            data = voice_record_event.data
            # Event data of signal containing succesful voice recording does not contain 'status' key.
            if 'status' not in data:
                self.misty.unregister_event('VoiceRecord')
                break

        # Process audio.
        audio = self.misty.get_audio_file('capture_Dialogue.wav', base64=True).json()['result']['base64']
        audio = base64.b64decode(audio)

        with open('output.wav', 'wb') as file:
            file.write(audio)

        r = sr.Recognizer()
        with sr.AudioFile('output.wav') as source:
            audio = r.record(source)
            try:
                text_result = r.recognize_google(audio)

                return text_result

            except sr.UnknownValueError as e:
                print("Unknown Value Error: " + str(e))

            except sr.RequestError as e:
                print("Request Error: " + str(e))


def main():
    mistyrobot = MistyRobot("192.168.43.66")
    name = mistyrobot.wait_for_face()
    # name = 'Sigur'

    # Seperate thread for face tracking to run parallel with rest of program.
    tracking_thread = threading.Thread(target=mistyrobot.track_face)
    tracking_thread.start()

    # mistyrobot.greet(name)

    ### If face recognition does not work, run start_script function manually like this:
    # mistyrobot.start_script1(formality='informal')

    mistyrobot.start_script1(name='Pepe', formality='informal')


    ### Uncomment the (parts of) the following code for set-up purposes

    # mistyrobot.misty.forget_faces()

    # mistyrobot.train_face('Simon')


if __name__ == '__main__':
    main()