from database.connection import get_db_connection
from models.magazine import Magazine
from models.author import Author

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        """
        Initializes an Article object with provided attributes.
        """
        self.id = id
        self._title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        if self.id is None:
            self.create_dtb_entry()

    @property
    def author(self):
        """
        Property method to retrieve the author of the article.
        """
        author_info = self.get_author_information_by_id(self.author_id)
        if author_info:
            return Author(author_info["id"], author_info['name'])
        else:
            return None

    @property
    def magazine(self):
        """
        Property method to retrieve the magazine of the article.
        """
        magazine_info = self.get_magazine_information_by_id(self.magazine_id)
        if magazine_info:
            return Magazine(magazine_info["id"], magazine_info['name'], magazine_info['category'])
        else:
            return None

    @property
    def title(self):
        return self._title

    @staticmethod
    def get_magazine_information_by_id(magazine_id):
        """
        Retrieves information about a magazine from the database based on their ID.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (magazine_id,))
        magazine_information = cursor.fetchone()
        conn.close()
        return magazine_information

    @title.setter
    def title(self, title):
        if not hasattr(self, '_title'):
            if isinstance(title, str) and 5 <= len(title) <= 50:
                self._title = title
            else:
                raise TypeError("Title must be a string containing 5 to 50 characters")
        else:
            raise AttributeError("Title cannot be modified")

    def create_dtb_entry(self):
        """
        Creates an entry in the database for the article.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       (self.title, self.content, self.author_id, self.magazine_id))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get_author_information_by_id(author_id):
        """
        Retrieves information about an author from the database based on their ID.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (author_id,))
        author_information = cursor.fetchone()
        conn.close()
        return author_information

    def __repr__(self):
      
        magazine_info = self.get_magazine_information_by_id(self.magazine_id)
        magazine_name = magazine_info['name'] if magazine_info else "No matches of the magazine's name provided found"
        author_info = self.get_author_information_by_id(self.author_id)
        author_name = author_info['name'] if author_info else "No matches of the author's name provided found"
       
        return f'Articles: {self.title} || Author: {author_name} || Magazine: {magazine_name}'