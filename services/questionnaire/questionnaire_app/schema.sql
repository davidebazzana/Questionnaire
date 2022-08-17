DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS ans_weight;
CREATE TABLE question (
    id INTEGER PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL,
    question_category TEXT NOT NULL,
    is_first_in_category INTEGER,
    is_first_in_group INTEGER,
    is_last_in_group INTEGER,
    group_description TEXT,
    number_of_answers_possible INTEGER,
    first_answer TEXT NOT NULL,
    second_answer TEXT NOT NULL,
    third_answer TEXT,
    fourth_answer TEXT,
    fifth_answer TEXT,
    sixth_answer TEXT
);
CREATE TABLE ans_weight (
    question_id INTEGER NOT NULL,
    answer_id INTEGER NOT NULL,
    science_weight INTEGER NOT NULL,
    art_weight INTEGER NOT NULL,
    FOREIGN KEY(question_id) REFERENCES question(id),
    PRIMARY KEY (question_id, answer_id)
);