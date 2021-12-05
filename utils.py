from config import mysql
import pymysql


def insert_db(table_name, json):
    conn = cursor = False
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        table_columns, values = list(json.keys()), list(json.values())
        sqlQuery = 'INSERT INTO %s(%s) VALUES("%s")' % (table_name, ','.join(table_columns), '","'.join([str(value) for value in values]))
        cursor.execute(sqlQuery)
        conn.commit()
        return False
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_db(table_name, columns, id, join='', where=''):
    conn = cursor = False
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT %s FROM %s %s %s" % (columns, table_name, join, where)
        if id:
            query += " WHERE id = %s" % id
        cursor.execute(query)
        rows = id and cursor.fetchone() or cursor.fetchall()
        return rows
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_db(table_name, json, id):
    conn = cursor = False
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        update_columns = ",".join([el + " = '" + json[el] + "'" for el in json.keys()])
        sqlQuery = "UPDATE %s SET %s WHERE id=%s" % (table_name, update_columns, id)
        cursor.execute(sqlQuery)
        conn.commit()
        return False
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_db(table_name, id):
    conn = cursor = False
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlQuery = "DELETE FROM %s WHERE id =%s" % (table_name, id)
        cursor.execute(sqlQuery)
        conn.commit()
        return False
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
