import sqlite3
from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category
        self.insert_magazine()

    def insert_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    def __repr__(self):
        return f'<Magazine {self._name}>'

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT DISTINCT a.* FROM authors a
                          JOIN articles ar ON a.id = ar.author_id
                          WHERE ar.magazine_id = ?''', (self._id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self._id,))
        article_titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return article_titles

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT a.*, COUNT(ar.author_id) as article_count FROM authors a
                          JOIN articles ar ON a.id = ar.author_id
                          WHERE ar.magazine_id = ?
                          GROUP BY ar.author_id
                          HAVING COUNT(ar.author_id) > 2''', (self._id,))
        contributing_authors = cursor.fetchall()
        conn.close()
        return contributing_authors
