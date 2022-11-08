import os


from dotenv import load_dotenv

load_dotenv()


def get_env_var(key: str) -> str | None:
    return os.getenv(key)
