import openai
import time
from rich.console import Console
from rich.text import Text
from io_service import IOService
from prompt_engine import PromptEngine

io = IOService()
prompt_engine = PromptEngine()
console = Console()


class OpenAIService:
    def __new__(self) -> None:
        if not hasattr(self, "instance"):
            self.instance = super(OpenAIService, self).__new__(self)
        return self.instance

    def check_if_key_exists(self) -> bool:
        json = io.read_json_file("config.json")
        key = json["openai_api_key"]
        if len(key) > 1 and key.startswith("sk-"):
            self.key = key
            openai.api_key = key
            return True
        else:
            return False

    def set_key(self, key) -> None:
        self.key = key
        openai.api_key = key

    def select_model(self) -> str:
        return io.select_model()

    def translate_text(self, text, language, model) -> str:
        if len(self.key) < 1:
            raise ValueError(
                "OpenAI API key was not provided. Use setKey to set a default API key first."
            )
        time.sleep(1)  # Rate limiting. Shouldn't be necessary. But just to be safe.
        chat_completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt_engine.get_default_translator_prompt(
                        language, text
                    ),
                }
            ],
        )
        translated_text = chat_completion.choices[0].message.content
        r_text = Text(text="\n")
        r_text.append("Translated ")
        r_text.append(text, style="bold yellow")
        r_text.append(" to ")
        r_text.append(translated_text, style="bold yellow")
        console.print(r_text)
        return translated_text
