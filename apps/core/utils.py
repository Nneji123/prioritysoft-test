import os


def read_code_sample(app_name: str, view_name: str, language: str):
    file_path = os.path.join(
        "./docs", "code_samples", app_name, view_name, f"{language}.txt"
    )
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Code sample for {language} not found."


def get_code_samples(app_name: str, view_name: str):
    languages = ["typescript", "javascript", "python", "dart", "curl"]
    return [
        {
            "lang": lang,
            "label": lang.capitalize(),
            "source": read_code_sample(app_name, view_name, lang),
        }
        for lang in languages
    ]
