import pymysql
from pymysql import cursors


class Database:
    connection_data = dict(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='taskwork'
    )

    def __init__(self):
        self.__database = pymysql.connect(**self.connection_data, cursorclass=cursors.DictCursor)
        self.__cursor = self.__database.cursor()
        self.create_table()

    def create_table(self):
        query = 'CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT, title VARCHAR(50), price INT, quantity INT, PRIMARY KEY (id))'
        args = ()
        self.__cursor.execute(query, args)
        return self.__database.commit()

    def get_product(self, **kwargs):
        query = "SELECT * FROM products WHERE "
        args = []
        args_str = []

        if not kwargs:
            return None

        for key, val in kwargs.items():
            args.append(val)
            args_str.append(f'{key} = %s')

        query += ' AND '.join(args_str)
        self.__cursor.execute(query, args)
        return self.__cursor.fetchone()

    def get_products(self, **kwargs):
        query = "SELECT * FROM products"
        args = []
        args_str = []

        if kwargs:
            query += ' WHERE '
            for key, val in kwargs.items():
                args.append(val)
                args_str.append(f'{key} = %s')

            query += ' AND '.join(args_str)

        self.__cursor.execute(query, args)
        return self.__cursor.fetchall()

    def add_product(self, **kwargs):
        query = 'INSERT INTO products ({}) VALUES ({})'
        args = []
        args_str = []

        if not kwargs:
            return None

        for key, val in kwargs.items():
            args.append(val)
            args_str.append(key)

        arg_patterns = ["%s" for _ in args]

        query = query.format(
            ', '.join(args_str),
            ', '.join(arg_patterns)
        )

        self.__cursor.execute(query, args)
        self.__database.commit()
        return self.__cursor.lastrowid

    def update_product(self, row_id: int, **kwargs):
        query = 'UPDATE products SET {} WHERE id = %s'
        args = []
        args_str = []

        if not kwargs:
            return

        for key, val in kwargs.items():
            args_str.append(f"{key} = %s")
            args.append(val)

        args.append(row_id)

        self.__cursor.execute(query, args)
        self.__database.commit()

    def delete_product(self, **kwargs):
        query = "DELETE FROM products WHERE "
        args = []
        args_str = []

        if not kwargs:
            return None

        for key, val in kwargs.items():
            args.append(val)
            args_str.append(f'{key} = %s')

        query += ' AND '.join(args_str)
        self.__cursor.execute(query, args)
        self.__database.commit()