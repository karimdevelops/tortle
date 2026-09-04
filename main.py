import time

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class Counter:
    def __init__(self) -> None:
        self.value = 0
        self.start_time = time.time()

    def increment(self):
        self.value += 1

    def reset(self):
        self.value = 0
        self.start_time = time.time()


counter = Counter()

app = FastAPI()


@app.middleware("http")
async def rate_limit(request: Request, call_next):

    counter.increment()
    current_time = time.time()
    elapsed_seconds = current_time - counter.start_time

    if elapsed_seconds > 60:
        counter.reset()

    if counter.value > 6:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Too many reqs"},
        )

    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {"msg": "HEllllooo!"}
