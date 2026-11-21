from fastapi import FastAPI

app = FastAPI(title="Keitaro Wrapper")


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}