from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating: Optional[int] = None 

while True:
    try:
        conn = psycopg.connect(host = os.getenv("HOST"), dbname=os.getenv("DATABASE"),user=os.getenv("USER"), password=os.getenv("PASSWORD"), row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successful!!!")
        break
    except Exception as error:
        print("Connection to Database failed.")
        print(f"Error: {error}")
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(payload: dict = Body(...)): # get data from body from fastApi and set it in payload in dict form
def create_posts(post:Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data" : "Created Post", "post" : new_post }

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    data = cursor.fetchone()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found')

    return {"post" : data}

@app.delete("/posts/{id}")
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""" , (id,))
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} exists")
    
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute(""" UPDATE posts  SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING * """, (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found')

    return {"message": "Post updated successfully", "updated_post": post}