from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating: Optional[int] = None 

my_posts = [{ "title" : "title of post 1", "content" : "content of post 1", "id" : 1}, { "title" : "fav food", "content" : "rajama chawal", "id" : 2}]

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(payload: dict = Body(...)): # get data from body from fastApi and set it in payload in dict form
def create_posts(post:Post):
    post_dict = post.model_dump()
    post_dict['id'] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {"data" : post_dict }

@app.get("/posts/{id}")
def get_post(id:int):
    data = next((p for p in my_posts if p["id"] == id), None)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with Id {id} was not found")
    return {"post" : data}

@app.delete("/posts/{id}")
def delete_post(id:int):
    post = next((p for p in my_posts if p["id"] == id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} exists")
    
    my_posts.remove(post)
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, updated_post:Post):
    index = next(
    (i for i, p in enumerate(my_posts) if p["id"] == id),None)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} exists")
    
    updated_post_dic = updated_post.model_dump()
    updated_post_dic['id'] = id

    my_posts[index] = updated_post_dic
    print(my_posts)

    return {"message": "Post updated successfully"}