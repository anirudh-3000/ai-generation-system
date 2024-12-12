import sqlite3

def init_db():
    """Initialize the database using schema.sql."""
    conn = sqlite3.connect("content_generation.db")
    cursor = conn.cursor()

    # Load schema from schema.sql
    with open("schema.sql", "r") as schema_file:
        cursor.executescript(schema_file.read())

    conn.commit()
    conn.close()

def insert_record(user_id, prompt, status="Processing"):
    """Insert a new record into the user_content table."""
    conn = sqlite3.connect("content_generation.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_content (user_id, prompt, video_paths, image_paths, status, generated_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (user_id, prompt, "", "", status))

    conn.commit()
    conn.close()

def update_record(user_id, video_paths, image_paths, status="Completed"):
    """Update record with generated file paths and status."""
    conn = sqlite3.connect("content_generation.db")
    cursor = conn.cursor()

    # Ensure video_paths and image_paths are lists, and default to empty string if empty
    video_paths_str = ",".join(video_paths) if video_paths else ""
    image_paths_str = ",".join(image_paths) if image_paths else ""

    cursor.execute("""
        UPDATE user_content
        SET video_paths = ?, image_paths = ?, status = ?
        WHERE user_id = ?
    """, (video_paths_str, image_paths_str, status, user_id))

    conn.commit()
    conn.close()


def fetch_record(user_id):
    """Fetch a record for a given user_id."""
    conn = sqlite3.connect("content_generation.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_content WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def log_activity(user_id, activity):
    """Log user activity such as login attempts and content views."""
    conn = sqlite3.connect("content_generation.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_activity (user_id, activity, timestamp)
        VALUES (?, ?, datetime('now'))
    """, (user_id, activity))

    conn.commit()
    conn.close()
