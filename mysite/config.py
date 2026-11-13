import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key-12345')
ALGORITHM = "HS256"
ACCESS_TOKEN_LIB = 30
REFRESH_TOKEN_LIB = 7