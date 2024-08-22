import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Books (
                            id INTEGER PRIMARY KEY,
                            title TEXT NOT NULL,
                            author TEXT NOT NULL,
                            status TEXT NOT NULL
                            )''')
        self.conn.commit()

    def add_book(self, title, author, status):
        self.cur.execute("INSERT INTO Books (title, author, status) VALUES (?, ?, ?)", (title, author, status))
        self.conn.commit()

    def fetch_all_books(self):
        self.cur.execute("SELECT * FROM Books")
        return self.cur.fetchall()

    def delete_book(self, book_id):
        self.cur.execute("DELETE FROM Books WHERE id=?", (book_id,))
        self.conn.commit()

    def update_book_status(self, book_id, status):
        self.cur.execute("UPDATE Books SET status=? WHERE id=?", (status, book_id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
