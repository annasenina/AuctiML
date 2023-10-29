import psycopg2
import urllib.request, json
from psycopg2.errorcodes import UNIQUE_VIOLATION

def connect_to_db():
    connection = psycopg2.connect(    # connection - это объект, который отвечает за соединение с БД
        database='AuctiML',         # database - это база данных (именно база, не СУБД)
        host='localhost',             # это говорит, что СУБД работает на моем компьютере
        user='user',              # имя пользователя
        password='postgres'           # пароль
        # port=5432,                  # порт не указываем, по умолчанию 5432
    )
    cursor = connection.cursor()      # cursor - это объект, который отвечает за взаимодействие с БД
    # Делаем запрос
    cursor.execute("""                   
    SELECT *
    FROM torgidata
    LIMIT 10
    """)
    results = cursor.fetchall()       # Получаем результаты (fetchall() - "получить всё")
    cursor.close()
    connection.close()
    return results                           # Это будет стандартный Python-объект. Не очень удобно, но работает
def insert_json_to_db(data:dict):
    connection = psycopg2.connect(  # connection - это объект, который отвечает за соединение с БД
        database='AuctiML',  # database - это база данных (именно база, не СУБД)
        host='localhost',  # это говорит, что СУБД работает на моем компьютере
        user='user',  # имя пользователя
        password='postgres'  # пароль
        # port=5432,                  # порт не указываем, по умолчанию 5432
    )
    cursor = connection.cursor()  # cursor - это объект, который отвечает за взаимодействие с БД
    # Делаем запрос
    try:
        cursor.execute(f"""                  
            INSERT
            INTO
            public.torgidata(lot_id, lot_data)
            values('{data['id']}', '[{json.dumps(data)}]')
            """)
        connection.commit()
    except psycopg2.Error as e:
        if e.pgcode == UNIQUE_VIOLATION:
            print("Лот с таким номером уже существует в базе ", data['id'],  e)
        else:
            print("Неизвестная ошибка парсинга лота", data['id'],  e)
    cursor.close()
    connection.close()

def download_json (url:str) -> dict:
    with urllib.request.urlopen(url) as url:
        data = json.load(url)
        return data

def parse_data (catCode: str):
    for i in range(0, 100):
        data_json = download_json("https://torgi.gov.ru/new/api/public/lotcards/search?catCode="+catCode+"&byFirstVersion=true&withFacets=true&page="+str(i)+"&size=100&sort=firstVersionPublicationDate,desc")
        for j in range(0, len(data_json["content"])):
            id = data_json["content"][j]["id"]
            lot_data = download_json("https://torgi.gov.ru/new/api/public/lotcards/"+str(id))
            insert_json_to_db(lot_data)
            print ("ready", i, j, id)



if __name__ == "__main__":
    #data_json = download_json("https://torgi.gov.ru/new/api/public/lotcards/22000061510000000025_2")
    parse_data("307")
    # print(len(data_json["content"]))
    #insert_json_to_db (data_json)
    #print (connect_to_db())
