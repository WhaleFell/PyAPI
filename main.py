import uvicorn
from fastapi import FastAPI
from routers import dy
from fastapi.responses import ORJSONResponse

app = FastAPI(debug=True)
app.include_router(dy.router)


@app.get("/")
async def root():
    return "PyAPI Welcome"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
