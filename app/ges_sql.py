import pymysql
import pymysql.cursors

def recup_id_user(username):
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_id FROM user WHERE username = %s"
            cursor.execute(sql, (username))
            result = cursor.fetchone()
    finally:
        connection.close()
    if result == None:
        return None
    for cle in result.values():
        return cle

def recup_last_id_create():
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT MAX(task_id) FROM task"
            cursor.execute(sql)
            result = cursor.fetchone()
        connection.commit()
    finally:
        connection.close()
    if result == None:
        return None
    for cle in result.values():
        return cle

def add_info_db_user(id, username, password):
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password))
        connection.commit()
    finally:
        connection.close()

def add_info_db_task(title, end, status, user_id):
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO task (title, end, status) VALUES (%s, %s, %s)"
            cursor.execute(sql, (str(title), end, str(status)))
        connection.commit()
    finally:
        connection.close()
    task_id = recup_last_id_create()
    add_info_db_user_has_task(user_id, task_id)

def add_info_db_user_has_task(user_id, task_id):
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO user_has_task (fk_user_id, fk_task_id) VALUES (%s, %s)"
            cursor.execute(sql, (user_id, task_id))
        connection.commit()
    finally:
        connection.close()

def recup_pass(table, username):
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT password FROM user WHERE username = %s"
            cursor.execute(sql, (username))
            result = cursor.fetchone()
    finally:
        connection.close()
    if result == None:
        return None
    for cle in result.values():
        return cle

def change_account_data(new_password, new_username, last_username):
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE user SET username = %s, password = %s WHERE username = %s"
            cursor.execute(sql, (new_username, new_password, last_username))
        connection.commit()
    finally:
        connection.close()

def change_task_data(id, new_title, new_end, new_status):
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE task SET title = %s, end = %s, status = %s WHERE id = %s"
            cursor.execute(sql, (new_title, new_end, new_status, id))
        connection.commit()
    finally:
        connection.close()

def delete_ligne_table_user(id):
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM user WHERE user_id = %s"
            cursor.execute(sql, (id))
        connection.commit()
    finally:
        connection.close()

def get_info_task(id):
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT title, end, status FROM task WHERE task_id = %s"
            cursor.execute(sql, (id))
            result = cursor.fetchone()
    finally:
        connection.close()
    return result

def get_id_user_task(id_user):
    connection = pymysql.connect(host = 'localhost',
                                user = 'root',
                                password = 'damien',
                                db = 'epytodo',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT fk_task_id FROM user_has_task WHERE fk_user_id = %s"
            cursor.execute(sql, (id_user))
            result = cursor.fetchone()
    finally:
        connection.close()
    return result
