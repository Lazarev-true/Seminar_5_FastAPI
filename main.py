from fastapi import FastAPI, Request, Form
from typing import Optional
from pydantic import BaseModel
import uvicorn
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

class User_in(BaseModel):
    name: str
    email: Optional[str]
    password: str

class User(User_in):
    id: int
    name: str
    email: str
    password: str

users = [
    User(id=1, name='user_1', email='1@ya.ru', password='4'),
    User(id=2, name='user_2', email='2@ya.ru', password='3'),
    User(id=3, name='user_3', email='3@ya.ru', password='2'),
    User(id=4, name='user_4', email='4@ya.ru', password='1'),
]

@app.get('/', response_model=list[User], summary='Получить всех пользователей', tags=['Получить'])
async def get_users():
    return users

@app.get('/get_html', response_class=HTMLResponse, summary='Получить шаблон', tags=['Получить'])
async def get_html(request: Request):
    title = "список пользователей"
    return templates.TemplateResponse('main.html', {'request':request, 'title': title, 'users': users})

@app.post('/user/new', response_class=User, summary='Добавляем нового пользователя', tags=['Добавить'])
async def ad_users(item: User_in):
    id = len(users) + 1
    user = User
    user.id = id
    user.name = item.name
    user.email = item.email
    user.password = item.password
    user.append(user)
    return user

def check_user_exist(id):
    for user in users:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail=f'Пользователь с таким {id} не найден')

@app.put('/user_put/{id}', response_class=User, summary='Изменить пользователя', tags=['Изменить'])
async def put_user(id: int, changed_user: User_in):
    user = check_user_exist(id)
    user.name = changed_user.name
    user.email = changed_user.email
    user.password = changed_user.password
    return user


@app.get('/user/{id}', response_class=User, summary='Получить пользователя по id', tags=['Получить'])
async def get_user_id(id: int):
    return check_user_exist(id)

@app.delete('/user_del/{id}', response_class=User, summary='УДалить пользователя по id', tags=['Удалить'])
async def delete_user_id(id: int):
    users.remove(check_user_exist(id))
    return users

if __name__ == '__main__':
    uvicorn.run("Flask_FastAPI_seminar_5:app", host="127.0.0.0", port=8000, reload=True )
