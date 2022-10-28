from flask import (
    Flask, Blueprint, g, request, render_template, redirect
)
from questionnaire_app.db import get_db
import os
import psycopg2
import atexit

NUMBER_OF_CLASSES = 4
CLASS = [
    "pratico", 
    "riflessivo",
    "critico",
    "razionale"
    ]

bp = Blueprint('questionnaire', __name__,
                        template_folder='templates')

try:
    conn = psycopg2.connect(dbname='log', 
                            user='mollami@mollami-log', 
                            host='mollami-log.postgres.database.azure.com', 
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

### REMOVE COMMENT BEFORE FLIGHT ###
atexit.register(close_connection_with_statistics_db)

@bp.route("/", methods=['GET'])
@bp.route("/questionnaire", methods=['GET'])
def get_questionnaire():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM question")
    questions = cursor.fetchall()
    ### REMOVE COMMENT BEFORE FLIGHT ###
    write_to_statistics("INSERT INTO visit (ts) VALUES (DEFAULT);")
    return render_template('questionnaire.html', questions=questions)

@bp.route("/result", methods=['GET'])
def get_result():
    db = get_db()
    cursor = db.cursor()
    personal_score = [0, 0, 0, 0]
    for question in request.args:
        cursor.execute(f"SELECT pratico_weight, riflessivo_weight, critico_weight, razionale_weight FROM ans_weight WHERE question_id = {question} AND answer_id = {request.args.get(question)}")
        weights = cursor.fetchone()
        for i in range(NUMBER_OF_CLASSES):
            personal_score[i] += weights[i]
        """
        print("-----------------------------------------------------------")
        print(f"question number: {question}")
        print(f"answer: {request.args.get(question)}")
        print(f"Pratico weight associated to question/answer: {weights[0]}")
        print(f"Riflessivo weight associated to question/answer: {weights[1]}")
        print(f"Critico weight associated to question/answer: {weights[2]}")
        print(f"Razionale weight associated to question/answer: {weights[3]}")
        print(f"Personal score: {personal_score}")
        print(f"Page to dislay: {CLASS[personal_score.index(max(personal_score))]}")
        print("-----------------------------------------------------------")
        """
    write_to_statistics(f"INSERT INTO log (ts, result) VALUES (DEFAULT, '{CLASS[personal_score.index(max(personal_score))]}');")
    return render_template(CLASS[personal_score.index(max(personal_score))] + ".html")

@bp.route("/critico", methods=['GET'])
def critic_profile():
    return render_template("critico.html")

@bp.route("/pratico", methods=['GET'])
def pratico_profile():
    return render_template("pratico.html")

@bp.route("/riflessivo", methods=['GET'])
def riflessivo_profile():
    return render_template("riflessivo.html")

@bp.route("/razionale", methods=['GET'])
def razionale_profile():
    return render_template("razionale.html")