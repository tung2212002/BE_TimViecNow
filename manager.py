import uvicorn
import multiprocessing
import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def main():
    multiprocessing.freeze_support()
    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True, workers=1)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
