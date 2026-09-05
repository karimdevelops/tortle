import time

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class Counter:
    def __init__(self) -> None:
        self.value = 0
        self.start_time = time.time()

    def increment(self):
        self.value += 1

    def reset(self):
        self.value = 0
        self.start_time = time.time()


counters: dict[str, Counter] = {}


class SlidingLogLimiter(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if not request.client:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "host doesn't exist"},
            )

        ip = request.client.host

        if ip not in counters:
            counter = Counter()
            counters[ip] = counter

        counters[ip].increment()

        current_time = time.time()
        elapsed_seconds = current_time - counters[ip].start_time

        if elapsed_seconds > 60:
            counters[ip].reset()

        if counters[ip].value > 6:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too many reqs"},
                headers={"Retry-After": f"{60 - elapsed_seconds}"},
            )

        response = await call_next(request)
        return response
