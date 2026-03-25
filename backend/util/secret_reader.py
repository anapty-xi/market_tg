import os

from dotenv import load_dotenv

load_dotenv()


def secret_reader(secret_name):
    """
    Получает секреты Docker
    """
    path = str(os.getenv(secret_name))
    with open(path) as f:
        secret_file = f.readline()

    return secret_file.strip()
