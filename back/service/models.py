from fastapi import FastAPI
from pydantic import BaseModel


class Url(BaseModel):
    url: str


app = FastAPI()  # noqa: pylint=invalid-name


@app.post("/predict")
def predict(data: Url):
    return "Вы ввели данные:  "+data.url+". Ваш запрос обрабатывается"
