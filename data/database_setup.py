import sqlite3


def create_users_db():
    try:
        conn = sqlite3.connect('user_credentials.db')
        cursor = conn.cursor()

        # Users table to store usernames and hashed passwords

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        ''')

        # Commit the changes and close the utilities
        conn.commit()
        conn.close()

        print("Users database created successfully!")

    except Exception as e:
        print("Error:", str(e))


def create_pacemaker_settings_db():
    try:
        conn = sqlite3.connect('pacemaker_settings.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS AAI (
                username TEXT PRIMARY KEY,
                LRL REAL DEFAULT NULL,
                URL REAL DEFAULT NULL,
                ARP REAL DEFAULT NULL,
                PVARP REAL DEFAULT NULL,
                H REAL DEFAULT NULL,
                AA REAL DEFAULT NULL,
                APW REAL DEFAULT NULL,
                "AS" REAL DEFAULT NULL,
                "RS" REAL DEFAULT NULL,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS AOO (
                username TEXT PRIMARY KEY,
                LRL REAL DEFAULT NULL,
                URL REAL DEFAULT NULL,
                APW REAL DEFAULT NULL,
                AA REAL DEFAULT NULL,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS VOO (
                username TEXT PRIMARY KEY,
                LRL REAL DEFAULT NULL,
                URL REAL DEFAULT NULL,
                VA REAL DEFAULT NULL,
                VPW REAL DEFAULT NULL,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS VVI (
                username TEXT PRIMARY KEY,
                LRL REAL DEFAULT NULL,
                URL REAL DEFAULT NULL,
                VRP REAL DEFAULT NULL,
                H REAL DEFAULT NULL,
                VA REAL DEFAULT NULL,
                VPW REAL DEFAULT NULL,
                VS REAL DEFAULT NULL,
                RS REAL DEFAULT NULL,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')

        # Commit the changes and close the utilities
        conn.commit()
        conn.close()

        print("Pacemaker Settings database created successfully!")

    except Exception as e:
        print("Error:", str(e))


create_users_db()
create_pacemaker_settings_db()