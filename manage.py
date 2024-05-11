import uvicorn
import multiprocessing


def main():
    multiprocessing.freeze_support()
    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True, workers=1)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
