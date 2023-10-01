from fastapi import FastAPI
from pydantic import BaseModel
from utils.validator import isURLValid
from model.predictForURL import predictForURL


class Url(BaseModel):
    url: str


app = FastAPI()  # noqa: pylint=invalid-name


@app.post("/predict")
def predict(data: Url):
    # Проверить, что url валидный
    if not isURLValid(data.url):
        "Указан неверный URL, попробуйте указать другой URL"
    # Предсказать данные по лоту
    return predictForURL(data.url)


