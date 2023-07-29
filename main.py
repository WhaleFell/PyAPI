import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import dy

app = FastAPI(debug=True)
app.include_router(dy.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "PyAPI Welcome"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
