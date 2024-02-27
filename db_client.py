import psycopg2
from psycopg2 import Error


# создание базы данных
def create_database():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="27738277",
            host="localhost",
            port="5432"
        )
        connection.autocommit = True
        cursor = connection.cursor()
        create_database_query = "CREATE DATABASE db_clients"
        cursor.execute(create_database_query)
        print("База данных успешно создана")
    except (Exception, Error) as error:
        print("Ошибка при создании базы данных:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# create_database


# подключения к базе данных
def connect_to_db():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="27738277",
            host="localhost",
            port="5432",
            database="db_clients"
        )
        return connection
    except (Exception, Error) as error:
        print("Ошибка при подключении к базе данных:", error)


# создание таблицы clients
def create_clients_table():
    try:
        connection = connect_to_db()
        connection.autocommit = True
        cursor = connection.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS clients
                                (id SERIAL PRIMARY KEY,
                                first_name TEXT,
                                last_name TEXT,
                                email TEXT)'''
        cursor.execute(create_table_query)
        print("Таблица clients успешно создана или уже существует")
    except (Exception, Error) as error:
        print("Ошибка при создании таблицы clients:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


create_clients_table()

# Функция для создания таблицы phones
def create_phones_table():
    try:
        connection = connect_to_db()
        connection.autocommit = True
        cursor = connection.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS phones
                                (id SERIAL PRIMARY KEY,
                                client_id INTEGER,
                                phone_number TEXT,
                                FOREIGN KEY (client_id) REFERENCES clients (id))'''
        cursor.execute(create_table_query)
        print("Таблица phones успешно создана или уже существует")
    except (Exception, Error) as error:
        print("Ошибка при создании таблицы phones:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


create_phones_table()


# добавление нового клиента
def add_client(first_name, last_name, email, phone=None):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO clients (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, email, phone))
        connection.commit()
        print("Новый клиент успешно добавлен")
    except (Exception, Error) as error:
        print("Ошибка при добавлении клиента:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


# добавление телефона для существующего клиента
def add_phone(client_id, phone):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE clients SET phone = %s WHERE id = %s", (phone, client_id))
        connection.commit()
        print("Телефон успешно добавлен для клиента с id", client_id)
    except (Exception, Error) as error:
        print("Ошибка при добавлении телефона:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


# изменение данных о клиенте
def update_client(client_id, first_name=None, last_name=None, email=None):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        if first_name:
            cursor.execute("UPDATE clients SET first_name = %s WHERE id = %s", (first_name, client_id))
        if last_name:
            cursor.execute("UPDATE clients SET last_name = %s WHERE id = %s", (last_name, client_id))
        if email:
            cursor.execute("UPDATE clients SET email = %s WHERE id = %s", (email, client_id))
        connection.commit()
        print("Данные о клиенте успешно обновлены")
    except (Exception, Error) as error:
        print("Ошибка при обновлении данных о клиенте:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


# удаление телефона для существующего клиента
def delete_phone(client_id):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE clients SET phone = NULL WHERE id = %s", (client_id,))
        connection.commit()
        print("Телефон успешно удален для клиента с id", client_id)
    except (Exception, Error) as error:
        print("Ошибка при удалении телефона:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


# удаление существующего клиента
def delete_client(client_id):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM clients WHERE id = %s", (client_id,))
        connection.commit()
        print("Клиент успешно удален")
    except (Exception, Error) as error:
        print("Ошибка при удалении клиента:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


# поиск клиента
def find_client(query):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clients WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR phone LIKE %s",
                       ('%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%'))
        result = cursor.fetchall()
        return result
    except (Exception, Error) as error:
        print("Ошибка при поиске клиента:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# ПОЕХАЛИ


add_client("Иван", "Петров", "ivan@mail.ru")

add_client("Петр", "Иванов", "petr@qoogle.com", "9168554236")

add_client("Мария", "Сидорова", "maria@mail.ru", "9058745521")

# Добавление телефона для клиента с id 1
add_phone(1, "9775314587")

# Добавление телефона для клиента с id 3
add_phone(3, "9168135541")

# Изменение имени клиента с id 1
update_client(1, first_name="Степан")

# Изменение фамилии клиента с id 2
update_client(2, last_name="Смирнов")

# Изменение email клиента с id 3
update_client(3, email="new_email@yandex.ru")

# Удаление телефона у клиента с id 1
delete_phone(1)

# Удаление клиента с id 2
delete_client(2)

# Поиск клиентов по имени
result1 = find_client("Иван")
print("Результат поиска клиентов по имени 'Иван':", result1)

# Поиск клиентов по фамилии "Иванов"
result2 = find_client("Петров")
print("Результат поиска клиентов по фамилии 'Петров':", result2)





