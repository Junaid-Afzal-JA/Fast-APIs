from fastapi import FastAPI, Depends, Path, status, Response, HTTPException
from models_db import models, schemas
from sqlalchemy.orm import session
from models_db.db_connection import engine, SessionLocal


app = FastAPI()
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=201)
def create_blog(request: schemas.Blog,
                db: session = Depends(get_db)):
    """
    Create Blog with specified title and description.

    Parameters:

        request (Blog): Blog to create.

    Returns:
        blg (Blog): Created blog information
    """
    blg = models.Blog(title=request.title,
                      description=request.description
                      )
    db.add(blg)
    db.commit()
    db.refresh(blg)
    return blg


@app.get('/blogs', status_code=200)
def get_all_blogs(db: session = Depends(get_db)) -> dict:
    """
    Return List of all blogs

    Parameters:

    Returns:

         blogs (Blog): All blogs data.
    """
    blogs = db.query(models.Blog).all()
    if blogs:
        return blogs
    else:
        HTTPException(status_code=404, detail='No Blog Data available.')


@app.get('/blogs/{blog_id}', status_code=status.HTTP_200_OK)
def get_specific_blog(
        response: Response,
        blog_id: int = Path(None, description='Id of blog you want to view.', gt=0),
        db: session = Depends(get_db)) -> dict:

    """
    Return Specific Blog

    Parameters:

        blog_id (int): Id of specific blog

    Returns:

         blog (Blog): Specific Blog data.
    """

    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog:
        return blog
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': 'No Blog Exist'}


@app.get('/blog-name', status_code=200)
def get_blog_by_name(
        blog_title: str,
        db: session = Depends(get_db)) -> dict:

    """
    Return Specific Blog

    Parameters:

        blog_title (str): Title of specific blog

    Returns:

         blog (Blog): Specific Blog data.
    """
    print('api title hit')
    blog = db.query(models.Blog).filter(models.Blog.title == blog_title).first()
    if blog:
        return blog
    else:
        raise HTTPException(status_code=404, detail=f'No Block exist with title {blog_title}')


@app.put('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, request: schemas.Blog, db: session = Depends(get_db)):
    """
    Update Blog specified with blog id.

    Parameters:

        blog_id (int): Id of blog to Update.
        request (Blog): Data to update.

    Returns:

        message (str):
    """
    print('in update')
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if blog.first():
        print('in if')
        blog.update({'title': request.title,
                     'description': request.description
                     }
                    )
        print('after update')
        db.commit()
        return {'detail': f'Blog with id {blog_id} Updated '}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No Blog Exist with id {blog_id}')


@app.delete('/blog/{blog_id}', status_code=204)
def delete_blog(blog_id: int, db: session = Depends(get_db)):
    """
    Delete Blog specified with blog id.

    Parameters:

        blog_id (int): Id of blog to delete.

    Returns:

        message (str):
    """
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if blog:
        blog.delete(synchronize_session=False)
        db.commit()
        return {'detail': f'Blog with id {blog_id} deleted '}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No Blog Exist with id {blog_id}')


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
