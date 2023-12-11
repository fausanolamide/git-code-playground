import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('Speak now...')
    try:
        # Adjust the timeout value as needed
        audio_text = r.listen(source, timeout=5)
        speech_text = r.recognize_google(audio_text)
        print('Speech recognized:', speech_text)
    except sr.WaitTimeoutError:
        print('Speech recognition timed out. No speech detected.')
    except sr.UnknownValueError:
        print('Could not understand audio')
    except sr.RequestError as e:
        print(
            f'Unable to get result from Google Speech Recognition service; {e}')

# Rest of your code...

    # tranlated_text = google_translator.translate(speech_text, lang_tgt="fr")
    # print(tranlated_text)
