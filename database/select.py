from pythonProject1.database.DBcm import DBContextManager


def select_list(db_config: dict, _sql: str):
    with DBContextManager(db_config=db_config) as cursor:
        if cursor is None:
            raise ValueError("Ошибка подключения к бд")  # передаем управление методу exit(), если подключение не создано
        else:
            cursor.execute(_sql)
            result = cursor.fetchall()  # cursor содержит description с именами полей, которые были в запросе выполнены
            print(cursor.description)
            schema = [item[0] for item in cursor.description]
            return result, schema


def select_dict(db_config: dict, _sql: str):
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    return result_dict