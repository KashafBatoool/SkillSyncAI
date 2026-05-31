-- SkillSync Database Schema
-- SQLite database structure for the SkillSync application

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    title TEXT,
    experience_level TEXT DEFAULT 'beginner',
    years_experience INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analyses table
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resume_text TEXT NOT NULL,
    job_description TEXT NOT NULL,
    ats_score REAL,
    matched_skills TEXT,
    missing_skills TEXT,
    excess_skills TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Skills table
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    category TEXT,
    proficiency INTEGER DEFAULT 50,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Recommendations table
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,
    course_title TEXT NOT NULL,
    platform TEXT,
    url TEXT,
    price REAL DEFAULT 0,
    duration TEXT,
    description TEXT,
    rating REAL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (analysis_id) REFERENCES analyses(id)
);

-- Career Predictions table
CREATE TABLE IF NOT EXISTS career_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    career_title TEXT NOT NULL,
    confidence REAL,
    description TEXT,
    salary_range TEXT,
    market_demand TEXT,
    required_skills TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Learning Plans table
CREATE TABLE IF NOT EXISTS learning_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan_name TEXT NOT NULL,
    target_role TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Learning Plan Items table
CREATE TABLE IF NOT EXISTS learning_plan_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    priority INTEGER DEFAULT 1,
    completed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES learning_plans(id),
    FOREIGN KEY (course_id) REFERENCES recommendations(id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_analyses_user_id ON analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_skills_user_id ON skills(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_analysis_id ON recommendations(analysis_id);
CREATE INDEX IF NOT EXISTS idx_career_predictions_user_id ON career_predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_plans_user_id ON learning_plans(user_id);
