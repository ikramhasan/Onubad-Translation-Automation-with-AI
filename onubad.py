from io_service import IOService
from openai_service import OpenAIService
from rich.progress import Progress

io = IOService()
open_ai = OpenAIService()


def translate():
    key_exists = open_ai.check_if_key_exists()
    if key_exists is not True:
        api_key = io.get_user_input("🔑 Open AI API key")
        open_ai.set_key(api_key)

    translation_dir = io.get_user_input("📁 Translation file directory")
    io.validate_dir_exists(translation_dir)
    base_file_name = io.choose_file(translation_dir)
    base_json_path = f"{translation_dir}/{base_file_name}"
    output_file_name = io.get_user_input("📋 Output file name")
    target_language = io.get_user_input("🈯 Target language")
    target_filename = f"{output_file_name}.json"
    target_json_path = f"{translation_dir}/{target_filename}"
    io.duplicate_file(base_json_path, target_json_path)
    target_json_file = io.read_json_file(path=target_json_path)
    model = open_ai.select_model()
    with Progress() as progress:
        tr_progress = progress.add_task(
            "[green]Translating...", total=len(target_json_file.keys())
        )
        for key in target_json_file.keys():
            target_json_file[key] = open_ai.translate_text(
                target_json_file[key], target_language, model
            )
            io.update_json_file(target_json_path, target_json_file)
            progress.update(tr_progress, advance=1)


if __name__ == "__main__":
    translate()
