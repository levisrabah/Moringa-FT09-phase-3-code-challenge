import unittest
from unittest.mock import patch, MagicMock
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")
        self.assertEqual(author.id, 1)

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.content, "Test Content")
        self.assertEqual(article.author_id, 1)
        self.assertEqual(article.magazine_id, 1)

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Tech")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Tech")

    @patch('models.article.get_db_connection')
    def test_article_author(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchone.return_value = {"id": 1, "name": "John Doe"}
        
        article = Article(1, "Test Title", "Test Content", 1, 1)
        author = article.author
        self.assertIsInstance(author, Author)
        self.assertEqual(author.name, "John Doe")

    @patch('models.article.get_db_connection')
    def test_article_magazine(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchone.return_value = {"id": 1, "name": "Tech Weekly", "category": "Tech"}
        
        article = Article(1, "Test Title", "Test Content", 1, 1)
        magazine = article.magazine
        self.assertIsInstance(magazine, Magazine)
        self.assertEqual(magazine.name, "Tech Weekly")

    @patch('models.magazine.get_db_connection')
    def test_articles(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = [
            {"id": 1, "title": "Article 1", "content": "Content 1", "author_id": 1, "magazine_id": 1},
            {"id": 2, "title": "Article 2", "content": "Content 2", "author_id": 2, "magazine_id": 1}
        ]
        
        magazine = Magazine(1, "Test Magazine", "Test Category")
        articles = magazine.articles
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].title, "Article 1")
        self.assertEqual(articles[1].title, "Article 2")

    @patch('models.magazine.get_db_connection')
    def test_contributors(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = [
            {"id": 1, "name": "John Doe"},
            {"id": 2, "name": "Jane Smith"}
        ]
        
        magazine = Magazine(1, "Test Magazine", "Test Category")
        contributors = magazine.contributors
        self.assertEqual(len(contributors), 2)
        self.assertEqual(contributors[0].name, "John Doe")
        self.assertEqual(contributors[1].name, "Jane Smith")

    @patch('models.magazine.get_db_connection')
    def test_article_titles(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = [
            {"id": 1, "title": "Article 1", "content": "Content 1", "author_id": 1, "magazine_id": 1},
            {"id": 2, "title": "Article 2", "content": "Content 2", "author_id": 2, "magazine_id": 1}
        ]
        
        magazine = Magazine(1, "Test Magazine", "Test Category")
        article_titles = magazine.article_titles()
        self.assertEqual(len(article_titles), 2)
        self.assertIn("Article 1", article_titles)
        self.assertIn("Article 2", article_titles)

    def setUp(self):
        self.magazine = Magazine(1, "Test Magazine", "Test Category")
        self.author1 = Author(1, "Author 1")
        self.author2 = Author(2, "Author 2")
        self.author3 = Author(3, "Author 3")

if __name__ == "__main__":
    unittest.main()
