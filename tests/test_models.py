from models.author import Author
from models.magazine import Magazine
from models.article import Article
from database.setup import create_tables
from database.connection import get_db_connection
import unittest

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_tables()

    def setUp(self):
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        conn.commit()
        conn.close()

       
        self.author1 = Author(None, "John Doe")
        self.author2 = Author(None, "Jane Smith")

        self.mag1 = Magazine(None, "Tech Monthly", "Technology")
        self.mag2 = Magazine(None, "Health Weekly", "Health")

        self.article1 = Article(None, "The Rise of AI", "Content about AI", self.author1.id, self.mag1.id)
        self.article2 = Article(None, "Healthy Eating Habits", "Content about healthy eating", self.author1.id, self.mag2.id)
        self.article3 = Article(None, "Quantum Computing", "Content about quantum computing", self.author2.id, self.mag1.id)
        self.article4 = Article(None, "The Future of Tech", "Content about the future of technology", self.author2.id, self.mag1.id)

    def test_author_creation(self):
        self.assertEqual(self.author1.name, "John Doe")
        self.assertEqual(self.author2.name, "Jane Smith")

    def test_article_creation(self):
        self.assertEqual(self.article1.title, "The Rise of AI")
        self.assertEqual(self.article2.title, "Healthy Eating Habits")

    def test_magazine_creation(self):
        self.assertEqual(self.mag1.name, "Tech Monthly")
        self.assertEqual(self.mag2.name, "Health Weekly")

    def test_author_articles(self):
        articles = self.author1.articles()
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].title, "The Rise of AI")
        self.assertEqual(articles[1].title, "Healthy Eating Habits")

    def test_author_magazines(self):
        magazines = self.author1.magazines()
        self.assertEqual(len(magazines), 2)
        self.assertEqual(magazines[0].name, "Tech Monthly")
        self.assertEqual(magazines[1].name, "Health Weekly")

    def test_magazine_articles(self):
        articles = self.mag1.articles()
        self.assertEqual(len(articles), 3)
        self.assertEqual(articles[0].title, "The Rise of AI")
        self.assertEqual(articles[1].title, "Quantum Computing")
        self.assertEqual(articles[2].title, "The Future of Tech")

    def test_magazine_contributors(self):
        contributors = self.mag1.contributors()
        self.assertEqual(len(contributors), 2)
        self.assertEqual(contributors[0].name, "John Doe")
        self.assertEqual(contributors[1].name, "Jane Smith")

    def test_magazine_article_titles(self):
        titles = self.mag1.article_titles()
        self.assertEqual(len(titles), 3)
        self.assertIn("The Rise of AI", titles)
        self.assertIn("Quantum Computing", titles)
        self.assertIn("The Future of Tech", titles)

    def test_magazine_contributing_authors(self):
        contributing_authors = self.mag1.contributing_authors()
        self.assertEqual(len(contributing_authors), 0)

    def test_article_author(self):
        self.assertEqual(self.article1.author.name, "John Doe")

    def test_article_magazine(self):
        self.assertEqual(self.article1.magazine.name, "Tech Monthly")

    def test_create_additional_article_for_author(self):
        article5 = Article(None, "New Health Trends", "Content about health trends", self.author1.id, self.mag2.id)
        articles = self.author1.articles()
        self.assertEqual(len(articles), 3)
        self.assertIn(article5.title, [article.title for article in articles])

    def test_create_additional_article_for_magazine(self):
        article5 = Article(None, "Future of Health Tech", "Content about health technology", self.author1.id, self.mag2.id)
        articles = self.mag2.articles()
        self.assertEqual(len(articles), 2)
        self.assertIn(article5.title, [article.title for article in articles])

    def test_magazine_contributing_authors_after_new_articles(self):
        article5 = Article(None, "AI and Health", "Content about AI in health", self.author2.id, self.mag1.id)
        contributing_authors = self.mag1.contributing_authors()
        self.assertEqual(len(contributing_authors), 1)
        self.assertEqual(contributing_authors[0].name, "Jane Smith")

    def test_delete_article_and_check_updates(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM articles WHERE id = ?', (self.article1.id,))
        conn.commit()
        conn.close()
        
        articles_by_author1 = self.author1.articles()
        self.assertEqual(len(articles_by_author1), 1)
        self.assertNotIn("The Rise of AI", [article.title for article in articles_by_author1])
        
        articles_in_mag1 = self.mag1.articles()
        self.assertEqual(len(articles_in_mag1), 2)
        self.assertNotIn("The Rise of AI", [article.title for article in articles_in_mag1])

if __name__ == "__main__":
    unittest.main()
