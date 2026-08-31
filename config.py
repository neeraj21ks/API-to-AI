import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST=os.getenv("DATABASE_HOST")
DATABASE_PORT=os.getenv("DATABASE_PORT")
DATABASE_NAME=os.getenv("DATABASE_NAME")
DATABASE_USER=os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
print(DATABASE_HOST)
print(DATABASE_PORT)
print(DATABASE_NAME)
print(DATABASE_USER)
def valid_config():
    if (DATABASE_HOST is None or DATABASE_PORT is None
    or DATABASE_NAME is None or DATABASE_USER is None
    or DATABASE_PASSWORD is None):
        missing=[]
        if DATABASE_HOST is None:
            missing.append("DATABASE_HOST")
        if DATABASE_NAME is None:
            missing.append("DATABASE_NAME")
        if DATABASE_PORT is None:
            missing.append("DATABASE_PORT")
        if DATABASE_USER is None:
            missing.append("DATABASE_USER")
        if DATABASE_PASSWORD is None:
            missing.append("DATABASE_PASSWORD")
        raise ValueError(
            f"missing required COnnfig variables":{','.join(missing)})