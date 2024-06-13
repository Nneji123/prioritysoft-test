import os
from datetime import datetime


def append_docstring_to_file(file_path, app_name):
    filename = os.path.basename(file_path)
    docstring = f'"""\n{filename} file for {app_name} app.\n\nAuthor(s): Ifeanyi Nneji\nDate: {datetime.now().strftime("%m/%d/%Y")}\n"""\n\n'

    with open(file_path, "r") as file:
        content = file.read()

    if not content.startswith('"""'):
        with open(file_path, "w") as file:
            file.write(docstring + content)


def traverse_and_append_docstring(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Skip the '__init__.py' files and 'migrations' directory
        if "__init__.py" in filenames:
            filenames.remove("__init__.py")
        if "migrations" in dirnames:
            dirnames.remove("migrations")

        app_name = os.path.basename(dirpath)
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                append_docstring_to_file(file_path, app_name)


# Example usage
root_directory = "./apps"
traverse_and_append_docstring(root_directory)
