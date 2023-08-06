from pathlib import Path
import shutil
import re


def path_to_pathlib(path):
    """
    If a string is passed to the function, it turns into Path from pathlib.
    :param path: string of path or Path from pathlib.
    """
    if isinstance(path, str):
        return Path(path)
    return path


def clear_directory(path):
    """
    This function clear directory with sub-directories
    :param path: path of directory from pathlib
    """
    path = path_to_pathlib(path)
    if path.is_dir():
        shutil.rmtree(path)  # Remove folder
    path.mkdir(parents=True, exist_ok=True)  # Add folder


def open_file(filename):
    """
    This function clear directory with sub-directories
    :param path: path of directory from pathlib
    """
    filename = path_to_pathlib(filename)
    s = ""
    with open(filename, 'r', encoding='utf8') as file:
        s = file.read()
    return s


def save_file(text, full_filename):
    filename = path_to_pathlib(full_filename)
    with open(filename, 'w', encoding='utf8') as file:
        file.write(text)


def remove_yaml_from_markdown(markdown_text):
    return re.sub(r'^---(.|\n)*?---\n', '', markdown_text.lstrip()).lstrip()
