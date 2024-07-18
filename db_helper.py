import sqlite3

class DBHelper:
    def __init__(self):
        self.conn = sqlite3.connect('quiz_app.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    first_name TEXT,
                    last_name TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    score INTEGER,
                    test_type TEXT
                )
            ''')
            self.conn.execute('''
                INSERT OR IGNORE INTO users (username, password, first_name, last_name) 
                VALUES ('admin', 'admin', 'Admin', 'User')
            ''')

    def get_user(self, username, password):
        cursor = self.conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        return cursor.fetchone()

    def insert_user(self, username, password, first_name, last_name):
        try:
            with self.conn:
                self.conn.execute('INSERT INTO users (username, password, first_name, last_name) VALUES (?, ?, ?, ?)', 
                                  (username, password, first_name, last_name))
            return True
        except sqlite3.IntegrityError:
            return False

    def insert_result(self, username, score, test_type):
        with self.conn:
            self.conn.execute('INSERT INTO results (username, score, test_type) VALUES (?, ?, ?)', 
                              (username, score, test_type))

    def get_results(self, filter_test=None, filter_username=None):
        query = 'SELECT * FROM results'
        conditions = []
        parameters = []

        if filter_test:
            conditions.append('test_type = ?')
            parameters.append(filter_test)
        
        if filter_username:
            conditions.append('username = ?')
            parameters.append(filter_username)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        cursor = self.conn.execute(query, parameters)
        return cursor.fetchall()
