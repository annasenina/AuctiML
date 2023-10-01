from back.service.utils.connectToDB import readLotFromDB, writeLoToDB

# ToDo написать функцию выделения id лота из строки
def getLotId(url: str) -> str:
    return ""

def predictForURL (url: str) -> str:


    lot = readLotFromDB(getLotId(url))

    # Лота нет в БД
    if lot == {}:
        # парсим данные с сайта
        # ToDo
        # делаем предсказания
        # ToDo
        # записываем в базу
        writeLoToDB(lot)
        return "По лоту не прошел аукцион, предсказанная стоимость лота = " + lot.predict
    else:
        # Лот есть в БД и по нему прошел аукцион
        if lot.cost != 0:
            return "По лоту уже прошел аукцион, стоимость лота = " + lot.cost
        # Лот есть в бд, по нему есть предсказания
        if lot.predict != 0:
            return "По лоту не прошел аукцион, предсказанная стоимость лота = " + lot.predict
        # Лот есть в бд, но по нему нет предсказаний
        # парсим данные с сайта
        # ToDo
        # делаем предсказания
        # ToDo
        # записываем в базу
        writeLoToDB(lot)
        return "По лоту не прошел аукцион, предсказанная стоимость лота = " + lot.predict


    return ""