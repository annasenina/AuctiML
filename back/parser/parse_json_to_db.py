import psycopg2
import urllib.request, json


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
    cursor.execute(f"""                  
        INSERT
        INTO
        public.torgidata(lot_id, lot_data)
        values('{data['id']}', '[{json.dumps(data)}]')
        """)
    connection.commit()
    cursor.close()
    connection.close()

def download_json (url:str ) -> dict:
    with urllib.request.urlopen(url) as url:
        data = json.load(url)
        return data

if __name__ == "__main__":
    data_json = download_json("https://torgi.gov.ru/new/api/public/lotcards/22000061510000000025_2")
    print (data_json["id"])
    insert_json_to_db (data_json)
    print (connect_to_db())
