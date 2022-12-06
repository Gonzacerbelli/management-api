import os
from dotenv import load_dotenv

load_dotenv()

def get_env_vars(var):
    env_vars = {
        "JWT_PUBLIC_KEY": os.getenv('JWT_PUBLIC_KEY'),
        "JWT_PRIVATE_KEY": os.getenv('JWT_PRIVATE_KEY'),
        "PUBLIC_ROUTES": os.getenv('PUBLIC_ROUTES')
    }

    return env_vars[var]