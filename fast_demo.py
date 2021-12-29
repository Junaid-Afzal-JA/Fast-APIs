from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    value: int


@app.post('/blog')
def create_blog(request: Blog):
    return request


@app.get('/')
def home() -> dict:
    """
    Return Home Page of Website.

    Parameters:

    Returns:
         result (dict): Response data in json format.
    """
    result = {'data': {'message': 'welcome to fastapi'}}
    return result


@app.get('/user')
def get_users():
    return {'data': 'List of all users'}


@app.get('/user/{uid}')
def get_specific_user(uid: int) -> dict:
    """
    Return data of specific user
    Parameters:
        uid (int): ID of user
    Returns:
        result (dict): Response in json format.
    """

    result = {'data': f'You are viewing profile of user {uid}'}
    return result

