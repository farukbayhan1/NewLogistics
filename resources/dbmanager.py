import sqlite3

def connect_db():
    connect = sqlite3.connect('resources/reading.db')
    return connect

def execute_query(query,params=(),fetchone=False,fetchall=False,commit=False):
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        result = None
        cursor.execute(query,params)
        if fetchone:
            result = cursor.fetchone()
        if fetchall:
            result = cursor.fetchall()
        if commit:
            result = conn.commit()
        return result
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()