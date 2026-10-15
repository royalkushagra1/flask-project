import sqlite3


# DATABASE = "cricket.db"


# def get_connection():
#     connection = sqlite3.connect(DATABASE)
#     connection.row_factory = sqlite3.Row
#     return connection



def create_users_table():
    connection = sqlite3.connect("cricket.db")
    # get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_users_table()
    print("Database and users table created successfully!")