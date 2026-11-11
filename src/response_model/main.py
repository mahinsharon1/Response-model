from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, EmailStr

app = FastAPI()

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    name: str

class UserIn(BaseUser):
    password: str

class UserOut(BaseUser):
    pass

users = {}

@app.post(
    "/users/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserIn):
    user_id = len(users) + 1
    users[user_id] = user.model_dump()

    return users[user_id]

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return users[user_id]


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    del users[user_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
