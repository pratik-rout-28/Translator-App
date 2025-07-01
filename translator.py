from deep_translator import GoogleTranslator
from langdetect import detect

def translate_text(text, dest_lang, src="auto"):
    try:
        if src == "auto":
            return GoogleTranslator(target=dest_lang).translate(text)
        else:
            return GoogleTranslator(source=src, target=dest_lang).translate(text)
    except Exception as e:
        print(f"[ERROR] translate_text failed: {e}")
        return "Error during translation: " + str(e)

def detect_language(text):
    if len(text.strip()) < 3:
        return "unknown"
    try:
        return detect(text)
    except Exception as e:
        print(f"[ERROR] detect_language failed: {e}")
        return "unknown"