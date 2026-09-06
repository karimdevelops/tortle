from fastapi import FastAPI

from tortle import FixedWindowLimiter

app = FastAPI()
app.add_middleware(FixedWindowLimiter, limit=8, window=120)


@app.get("/")
async def root():
    return {"msg": "hello!"}
