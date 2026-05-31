"""
Database Initialization Script - Set up SkillSync database
"""
import sqlite3
import os
from pathlib import Path


def init_database(db_path: str = "database/skillsync.db") -> None:
    """
    Initialize the SkillSync database with schema
    
    Args:
        db_path: Path to the SQLite database file
    """
    # Create database directory if it doesn't exist
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)
    
    # Read schema
    schema_path = Path(__file__).parent / "schema.sql"
    
    if not schema_path.exists():
        print(f"Schema file not found at {schema_path}")
        return
    
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    # Connect and initialize
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Execute schema
        cursor.executescript(schema)
        conn.commit()
        print(f"✅ Database initialized successfully at {db_path}")
    
    except sqlite3.Error as e:
        print(f"❌ Database initialization failed: {e}")
        conn.rollback()
    
    finally:
        conn.close()


def add_sample_data(db_path: str = "database/skillsync.db") -> None:
    """
    Add sample data to the database
    
    Args:
        db_path: Path to the SQLite database file
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Sample users
        users = [
            ("user1", "John Doe", "john@example.com", "Senior Developer"),
            ("user2", "Jane Smith", "jane@example.com", "Product Manager"),
            ("user3", "Bob Johnson", "bob@example.com", "Junior Developer"),
        ]
        
        cursor.executemany(
            "INSERT INTO users (username, name, email, title) VALUES (?, ?, ?, ?)",
            users
        )
        
        # Sample analyses
        analyses = [
            (1, "Resume 1", "Job 1", 85.5, "completed"),
            (2, "Resume 2", "Job 2", 72.0, "completed"),
        ]
        
        cursor.executemany(
            "INSERT INTO analyses (user_id, resume_text, job_description, ats_score, status) VALUES (?, ?, ?, ?, ?)",
            analyses
        )
        
        # Sample skills
        skills = [
            (1, "Python", "Technical", 90),
            (1, "SQL", "Technical", 85),
            (1, "Leadership", "Soft Skill", 80),
            (2, "Project Management", "Soft Skill", 95),
            (2, "Excel", "Technical", 88),
            (3, "JavaScript", "Technical", 70),
            (3, "React", "Technical", 65),
        ]
        
        cursor.executemany(
            "INSERT INTO skills (user_id, skill_name, category, proficiency) VALUES (?, ?, ?, ?)",
            skills
        )
        
        conn.commit()
        print("✅ Sample data added successfully")
    
    except sqlite3.Error as e:
        print(f"❌ Failed to add sample data: {e}")
        conn.rollback()
    
    finally:
        conn.close()


def reset_database(db_path: str = "database/skillsync.db") -> None:
    """
    Reset the database (delete and reinitialize)
    
    Args:
        db_path: Path to the SQLite database file
    """
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Deleted existing database at {db_path}")
    
    init_database(db_path)
    add_sample_data(db_path)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize SkillSync database")
    parser.add_argument("--reset", action="store_true", help="Reset database")
    parser.add_argument("--sample", action="store_true", help="Add sample data")
    parser.add_argument("--db", default="database/skillsync.db", help="Database path")
    
    args = parser.parse_args()
    
    if args.reset:
        reset_database(args.db)
    else:
        init_database(args.db)
        if args.sample:
            add_sample_data(args.db)
