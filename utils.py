from config import mysql
import pymysql


def execute_query(sqlQuery,type_cursor=False, with_rows=False, single_row=False):
    conn = cursor = False
    try:
        conn = mysql.connect()
        if type_cursor:
            cursor = conn.cursor(type_cursor)
        else:
            cursor = conn.cursor()
        cursor.execute(sqlQuery)
        conn.commit()
        if with_rows:
            rows = single_row and cursor.fetchone() or cursor.fetchall()
            return rows
        return False
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_db(table_name, json):
    table_columns, values = list(json.keys()), list(json.values())
    sqlQuery = 'INSERT INTO %s(%s) VALUES("%s")' % (table_name, ','.join(table_columns), '","'.join([str(value) for value in values]))
    return execute_query(sqlQuery)


def update_db(table_name, json, id):
    update_columns = ",".join([el + " = '" + json[el] + "'" for el in json.keys()])
    sqlQuery = "UPDATE %s SET %s WHERE id=%s" % (table_name, update_columns, id)
    return execute_query(sqlQuery)


def delete_db(table_name, id):
    sqlQuery = "DELETE FROM %s WHERE id =%s" % (table_name, id)
    return execute_query(sqlQuery)


def get_db(table_name, columns, id, join='', where=''):
    query = "SELECT %s FROM %s %s %s" % (columns, table_name, join, where)
    if id:
        query += " WHERE id = %s" % id
    return execute_query(query, pymysql.cursors.DictCursor,True, id)
