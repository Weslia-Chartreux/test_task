from pydantic import BaseModel


class AuthModel(BaseModel):
    name: str
    password: str


class CreatePostModel(BaseModel):
    title: str
    content: str


class PatchPostModel(BaseModel):
    title: str = None
    content: str = None

