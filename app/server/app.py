from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from routes.users import router as userRouter

app = FastAPI()

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


app.include_router(userRouter, tags=["User"], prefix="/user")

