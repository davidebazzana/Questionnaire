from flask import (
    Flask, Blueprint, g, request, render_template, redirect
)
from questionnaire_app.db import get_db
import os
import psycopg2
import atexit

NUMBER_OF_CLASSES = 2
CLASS_PAGE = [
    "science_guy.html", 
    "art_guy.html"
    ]

bp = Blueprint('questionnaire', __name__,
                        template_folder='templates')

"""
try:
    conn = psycopg2.connect(dbname='mollami-data', 
                            user='mollami@mollami-data-server', 
                            host='mollami-data-server.postgres.database.azure.com', 
                            password=os.environ.get("STATISTICS_DB_PASSWORD"), 
                            port='5432', 
                            sslmode='require')
except:
    print("Unable to reach mollami-data-server.postgres.database.azure.com")

def write_to_statistics(query):
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    print("Performed query: " + query)

def close_connection_with_statistics_db():
    conn.close()
    print("Successfully closed connection with mollami-data-server.postgres.database.azure.com")

atexit.register(close_connection_with_statistics_db)
"""

@bp.route("/", methods=['GET'])
@bp.route("/questionnaire", methods=['GET'])
def get_questionnaire():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM question")
    questions = cursor.fetchall()
    # write_to_statistics("INSERT INTO visit VALUES (DEFAULT, DEFAULT);")
    return render_template('questionnaire.html', questions=questions)

@bp.route("/result", methods=['GET'])
def get_result():
    db = get_db()
    cursor = db.cursor()
    personal_score = [0, 0]
    for question in request.args:
        cursor.execute(f"SELECT science_weight, art_weight FROM ans_weight WHERE question_id = {question} AND answer_id = {request.args.get(question)}")
        weights = cursor.fetchone()
        for i in range(NUMBER_OF_CLASSES):
            personal_score[i] += weights[i]
        """
        print("-----------------------------------------------------------")
        print(f"question number: {question}")
        print(f"answer: {request.args.get(question)}")
        print(f"Science weight associated to question/answer: {weights[0]}")
        print(f"Art weight associated to question/answer: {weights[1]}")
        print(f"Personal score: {personal_score}")
        print("-----------------------------------------------------------")
        """
    return render_template(CLASS_PAGE[personal_score.index(max(personal_score))])

@bp.route("/profile_test", methods=['GET'])
def profile_test():
    return render_template("critic.html")