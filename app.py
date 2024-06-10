from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Connect to the database
    session = get_db_connection()

    # Create an author
    author = Author(id=None, name="John Doe")
    print(f"Created Author: {author}")

    # Create a magazine
    magazine = Magazine(id=None, name="Tech Today", category="Technology")
    print(f"Created Magazine: {magazine}")

    # Create an article
    article = Article(id=None, title="The Rise of AI", content="Content about AI", author_id=author.id, magazine_id=magazine.id)
    print(f"Created Article: {article}")

    # Query the database for inserted records
    authors = session.query(Author).all()
    magazines = session.query(Magazine).all()
    articles = session.query(Article).all()

    # Display results
    print("\nAuthors:")
    for author in authors:
        print(author)

    print("\nMagazines:")
    for magazine in magazines:
        print(magazine)

    print("\nArticles:")
    for article in articles:
        print(article)

if __name__ == "__main__":
    main()
