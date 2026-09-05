from fastapi import FastAPI

from tortle import SlidingLogLimiter

app = FastAPI()
app.add_middleware(SlidingLogLimiter)


@app.get("/")
async def root():
    return {"msg": "hello!"}
