import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Creates and returns a MySQL database connection.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "tech_market_intelligence_db"),
        )
        return connection
    except mysql.connector.Error as error:
        raise RuntimeError(f"Database connection failed: {error}")