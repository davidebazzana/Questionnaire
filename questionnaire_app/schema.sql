CREATE TABLE IF NOT EXISTS question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL,
    first_answer TEXT NOT NULL,
    second_answer TEXT NOT NULL,
    third_answer TEXT,
    fourth_answer TEXT,
    fifth_answer TEXT,
    sixth_answer TEXT
);
CREATE TABLE IF NOT EXISTS answer (
    question_id INTEGER,
    answer_id INTEGER,
    science_weight INTEGER,
    art_weight INTEGER,
    FOREIGN KEY(question_id) REFERENCES question(id),
    PRIMARY KEY (question_id, answer_id)
);