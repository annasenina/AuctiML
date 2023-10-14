import psycopg2


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
    results                           # Это будет стандартный Python-объект. Не очень удобно, но работает

if __name__ == "__main__":
    connect_to_db()