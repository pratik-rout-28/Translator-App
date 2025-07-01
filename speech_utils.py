from gtts import gTTS

def text_to_speech(text, lang='en', filename='translated.mp3'):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename
