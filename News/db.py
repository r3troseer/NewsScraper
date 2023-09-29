import psycopg2
from decouple import config
from recent_paper import get_recent_articles

vanguard_url = "https://www.vanguardngr.com/category/top-stories/"

# Database connection parameters
db_params = {
    "dbname": config("DB_NAME"),
    "user": config("DB_USERNAME"),
    "password": config("DB_PASSWORD"),
    "host": config("DB_HOSTNAME"),
    "port": config("DB_PORT", cast=int),
}


def create_article_table(conn):
    """Create the article table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        # SQL statement to create the article table
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                title TEXT,
                text TEXT,
                url TEXT
            )
        """
        cursor.execute(create_table_sql)
        conn.commit()
        cursor.close()
    except Exception as e:
        print("Error creating article table:", e)


def save_article(conn, title, text, url):
    """Save an article to the database."""
    try:
        cursor = conn.cursor()
        # SQL statement to insert an article into the table
        insert_article_sql = """
            INSERT INTO articles (title, text, url)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_article_sql, (title, text, url))
        conn.commit()
        cursor.close()
    except Exception as e:
        print("Error saving article:", e)


if __name__ == "__main__":
    # Connect to the PostgreSQL database
    try:
        conn = psycopg2.connect(**db_params)
        print(conn)
        create_article_table(conn)  # Create the article table if it doesn't exist

        articles = get_recent_articles(vanguard_url, max_age_days=4)

        for article_data in articles:
            save_article(
                conn, article_data["title"], article_data["text"], article_data["url"]
            )

        conn.close()
    except Exception as e:
        print("Error connecting to the database:", e)
