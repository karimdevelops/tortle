from fastapi import FastAPI

from tortle import SlidingLogLimiter

app = FastAPI()
app.add_middleware(SlidingLogLimiter, limit=1, window=120)


@app.get("/")
async def root():
    return {"msg": "hello!"}
