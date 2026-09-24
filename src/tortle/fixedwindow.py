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


class FixedWindowLimiter(BaseHTTPMiddleware):
    def __init__(self, app, limit, window):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.counters: dict[str, Counter] = {}

    async def dispatch(self, request: Request, call_next):

        if not request.client:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Host doesn't exist"},
            )

        ip = request.client.host

        if ip not in self.counters:
            counter = Counter()
            self.counters[ip] = counter

        self.counters[ip].increment()

        current_time = time.time()
        elapsed_seconds = current_time - self.counters[ip].start_time

        if elapsed_seconds > self.window:
            self.counters[ip].reset()

        if self.counters[ip].value > self.limit:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too many reqs"},
                headers={
                    "Retry-After": f"{60 - round(elapsed_seconds, 1)}"
                },
            )

        response = await call_next(request)
        return response
