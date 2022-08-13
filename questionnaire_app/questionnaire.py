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
    return render_template('questionnaire.html')

@bp.route("/result", methods=['GET'])
def get_result():
    i_question = 0
    personal_score = [0, 0]
    for question in request.args:
        for i in range(NUMBER_OF_CLASSES):
            personal_score[i] += WEIGHT_VECTORS[i_question][int(request.args.get(question))][i]
        i_question += 1
    return render_template(CLASS_PAGE[personal_score.index(max(personal_score))])