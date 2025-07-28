# db/sql_connector.py

import pyodbc

def get_admin_by_id(admin_id):
    try:
        conn = pyodbc.connect(
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=OMEN\SQLEXPRESS;'
            r'DATABASE=myappDB_test;'
            r'Trusted_Connection=yes;'
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, password, current_status, new_status FROM dbo.admin_info WHERE admin_id = ?", admin_id
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "username": row[0],
                "password": row[1],
                "current_status": row[2],
                "new_status": row[3],
            }
        return None
    except Exception as e:
        print(f"DB error: {e}")
        return None
