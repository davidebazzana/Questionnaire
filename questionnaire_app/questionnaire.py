from flask import (
    Flask, Blueprint, g, request, render_template, redirect
)
from questionnaire_app.db import get_db

NUMBER_OF_CLASSES = 2
# [science_guy, art_guy]
# All the scores go from 0 to 10
WEIGHT_VECTORS = [
    [[8, 2], [4, 6], [6, 4], [2, 8]],
    [[2, 8], [4, 6], [6, 4], [8, 2]],
    [[9, 5], [1, 5], [5, 5]],
    [[1, 1], [2, 2], [7, 7], [8, 8], [9, 9]],
    [[1, 1], [2, 2], [7, 7], [8, 8], [9, 9]]
    ]
CLASS_PAGE = [
    "science_guy.html", 
    "art_guy.html"
    ]

bp = Blueprint('questionnaire', __name__,
                        template_folder='templates')

@bp.route("/", methods=['GET'])
@bp.route("/questionnaire", methods=['GET'])
def get_questionnaire():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM question")
    questions = cursor.fetchall()
    return render_template('questionnaire.html', questions=questions)

@bp.route("/result", methods=['GET'])
def get_result():
    db = get_db()
    cursor = db.cursor()
    i_question = 0
    personal_score = [0, 0]
    for question in request.args:
        print(f"question number: {question}")
        print(f"answer: {request.args.get(question)}")
        cursor.execute(f"SELECT science_weight, art_weight FROM ans_weight WHERE question_id = {question} AND answer_id = {request.args.get(question)}")
        weights = cursor.fetchone()
        for i in range(NUMBER_OF_CLASSES):
            personal_score[i] += weights[i]
        print(f"Science weight associated to question/answer: {weights[0]}")
        print(f"Art weight associated to question/answer: {weights[1]}")
        print(f"Personal score: {personal_score}")
        i_question += 1
    return render_template(CLASS_PAGE[personal_score.index(max(personal_score))])