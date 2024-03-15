from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def say_hello() -> dict[str, str]:
    return {'message': 'Hello World'}
