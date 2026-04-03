from fastapi import FastAPI

app = FastAPI(title="POS System API")


@app.get("/health")
def health_check():
    return {"status": "ok"}