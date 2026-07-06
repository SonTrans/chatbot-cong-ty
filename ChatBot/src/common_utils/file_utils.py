import os
import shutil
import time

import requests

from src.config.configs import config_object

class InputFileException(Exception):
    pass

DATA_DIR = getattr(config_object, "LOG", type('obj', (object,), {'LOG_DIR': './data'}))
# Just hardcode a temp dir for now to match the old pattern safely
TEMP_DIR = os.path.join(getattr(config_object, "DATA_DIR", "./data"), 'temp')

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR, exist_ok=True)


def save_fastapi_request_file(url_file):
    filename = url_file.filename
    extension = filename[filename.rfind('.'):].lower()

    timestamp = time.time_ns()
    file = os.path.join(TEMP_DIR, f'{timestamp}{extension}')
    if os.path.isfile(file):
        timestamp += 1
        file = os.path.join(TEMP_DIR, f'{timestamp}{extension}')
    with open(file, "wb") as buffer:
        shutil.copyfileobj(url_file.file, buffer)

    if file is None:
        raise InputFileException()
    return file


def delete_file(filepath):
    if filepath is not None and (os.path.isfile(filepath) or os.path.islink(filepath)):
        os.unlink(filepath)

def download_image(url, save_path=None):
    if save_path is None:
        extension = url[url.rfind('.'):].lower()
        timestamp = time.time_ns()
        save_path = os.path.join(TEMP_DIR, f'{timestamp}{extension}')
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    return save_path
