import os
from dotenv import load_dotenv

def get_jwt_token():
    env_path = os.path.join(os.path.dirname(__file__), "example.env")
    load_dotenv(dotenv_path=env_path)
    jwt_token = os.getenv("SECRET_KEY")
    if jwt_token is None:
        raise ValueError("JWT token not found in environment variables.")
    return jwt_token