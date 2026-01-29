import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import get_settings
from contextlib import contextmanager

settings = get_settings()

# Parse connection string
def get_connection():
    """Get a database connection"""
    try:
        conn = psycopg2.connect(settings.database_url)
        return conn
    except Exception as e:
        raise Exception(f"Failed to connect to database: {str(e)}")

def init_db():
    """Initialize database with tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(255) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'user' NOT NULL,
                full_name VARCHAR(255),
                is_active BOOLEAN DEFAULT true NOT NULL,
                created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP DEFAULT NOW() NOT NULL
            )
        """)
        
        # Create uploads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                file_path VARCHAR(255) NOT NULL,
                cloth_type VARCHAR(50) NOT NULL,
                occasion VARCHAR(50) NOT NULL,
                gender VARCHAR(50) NOT NULL,
                age_group VARCHAR(50) NOT NULL,
                budget_range VARCHAR(50) NOT NULL,
                size_info VARCHAR(255),
                created_at TIMESTAMP DEFAULT NOW() NOT NULL
            )
        """)
        
        # Create design_suggestions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS design_suggestions (
                id SERIAL PRIMARY KEY,
                upload_id INTEGER NOT NULL REFERENCES uploads(id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                neck_design VARCHAR(255) NOT NULL,
                sleeve_style VARCHAR(255) NOT NULL,
                embroidery_pattern VARCHAR(255) NOT NULL,
                color_combination VARCHAR(255) NOT NULL,
                border_style VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                confidence_score VARCHAR(50) DEFAULT 'High' NOT NULL,
                created_at TIMESTAMP DEFAULT NOW() NOT NULL
            )
        """)
        
        # Create saved_designs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_designs (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                design_suggestion_id INTEGER NOT NULL REFERENCES design_suggestions(id) ON DELETE CASCADE,
                saved_at TIMESTAMP DEFAULT NOW() NOT NULL
            )
        """)
        
        conn.commit()
        print("Database tables initialized successfully")
    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to initialize database: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def get_db():
    """Dependency to get database connection"""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_db_cursor(conn):
    """Context manager for database cursor"""
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()

# For compatibility with existing code
class Base:
    """Dummy Base class for compatibility"""
    class metadata:
        @staticmethod
        def create_all(bind=None):
            """Initialize database"""
            init_db()

Base = Base()

# For compatibility
engine = None
