-- Table to store user content information
CREATE TABLE IF NOT EXISTS user_content (
    user_id TEXT PRIMARY KEY,  -- Unique identifier for the user
    prompt TEXT,               -- The text prompt provided by the user
    video_paths TEXT,          -- Comma-separated list of paths to generated videos
    image_paths TEXT,          -- Comma-separated list of paths to generated images
    status TEXT,               -- Generation status ("Processing" or "Completed")
    generated_at TEXT         -- Timestamp when the content was generated
);

-- Table to log user activity (login attempts and content views)
CREATE TABLE IF NOT EXISTS user_activity (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,              -- Foreign key to user_id
    activity TEXT,             -- Type of activity (Login, View)
    timestamp TEXT,            -- Time of activity
    FOREIGN KEY (user_id) REFERENCES user_content (user_id)
);

select * from user_content;

select * from user_activity

