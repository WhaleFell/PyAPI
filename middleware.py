import time
from fastapi import Request


class ProcessTimerMiddleware(object):
    """
    Record when the request was processed and write to headers
    """

    def __init__(
            self,
    ):
        pass

    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        # process the request and get the response
        response = await call_next(request)
        process_time = time.time() - start_time
        # do something with the request object
        response.headers["X-Process-Time"] = str(process_time)
        return response
