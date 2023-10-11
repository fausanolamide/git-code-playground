import speech_recognition as sr
from google_trans_new import google_translator
r = sr.Recognizer()

with sr.Microphone() as source:
    print('speak now')
    audio_text = r.listen(source)
    try:
        speech_text = r.recognize_google(audio_text)
        print(speech_text)
    except sr.UnknownValueError:
        print("Could not understand")
    except sr.RequestError:
        print("Unable to get result from google")

    # tranlated_text = google_translator.translate(speech_text, lang_tgt="fr")
    # print(tranlated_text)
