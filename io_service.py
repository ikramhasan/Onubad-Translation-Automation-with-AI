import json
import shutil
import os
import inquirer
from rich.console import Console
from rich.prompt import Prompt
from rich.tree import Tree
from rich import print
from rich.panel import Panel

console = Console()


class IOService:
    def get_user_input(self, prompt) -> str:
        return Prompt.ask(f"[bold green ]{prompt}")

    def validate_dir_exists(self, dir):
        exists = os.path.isdir(dir)
        if exists:
            tree = Tree(dir)
            files = os.listdir(dir)
            for file in files:
                tree.add(file)
            print(Panel(tree, title="Files found in directory"))
            return True
        else:
            console.print("Directory does not exist!", style="bold red")
            exit(0)

    def choose_file(self, dir) -> str:
        files = os.listdir(dir)
        console.print("[bold green ]Choose the base JSON file you want to translate")
        questions = [
            inquirer.List(
                "file",
                message="Selected file",
                choices=files,
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers["file"]

    def select_model(self) -> str:
        console.print(
            "[bold green ]Select the OpenAI model you want to use. Note: gpt-4 may not be available for your  account."
        )
        questions = [
            inquirer.List(
                "model",
                message="Selected model",
                choices=["gpt-4", "gpt-3.5-turbo"],
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers["model"]

    def duplicate_file(self, og_file_path, new_file_path) -> None:
        shutil.copy2(og_file_path, new_file_path)

    def read_json_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def update_json_file(self, filepath, json_file):
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(json_file, file, ensure_ascii=False, indent=4)
