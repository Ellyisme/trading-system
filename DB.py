import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user='root',
        passwd="password123",
        database="masy",
        auth_plugin="caching_sha2_password"
    )
