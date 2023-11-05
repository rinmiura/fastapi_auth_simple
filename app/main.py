from typing import Optional, Annotated

from fastapi import FastAPI, Response, Form, HTTPException, Depends, Cookie, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from db.utils import get_user, generate_session_token, check_user, hash_password, register_user

app = FastAPI()

security = HTTPBasic()


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user(credentials.username, credentials.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


@app.post("/login/")
async def login(response: Response,
                username: str = Form(...),
                password: str = Form(...)):
    user = get_user(username, password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    response.set_cookie("session_token", generate_session_token(), secure=True, httponly=True)
    return {"message": "login successful"}


@app.post("/register/")
async def register(response: Response,
                   username: str = Form(...),
                   password: str = Form(...)):
    user = check_user(username)
    if user is None:
        hashed = hash_password(password)
        register_user(username, hashed)
        response.set_cookie("session_token", generate_session_token(), secure=True, httponly=True)
        return {"message": f"User {username} successfully created."}
    else:
        raise HTTPException(status_code=400, detail=f"User {username} already exists.")


@app.get("/protected")
async def protected_route(user: dict = Depends(authenticate_user),
                          session_token: Optional[str] = Cookie(default=None)):
    if session_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
