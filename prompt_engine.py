class PromptEngine:
    def get_default_translator_prompt(self, language, text):
        return f"Suppose you are an amazing professional translator who's job is to translate any given text properly. You will be given a text to translate. You have to translate it to {language} language. Respond with the translated text and nothing else. Text: {text}"
