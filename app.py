from flask import (
    Flask, request, render_template, redirect
)

app = Flask(__name__)

NUMBER_OF_CLASSES = 2
WEIGHT_VECTORS = [
    [[8, 2], [4, 6], [6, 4], [2, 8]],
    [[2, 8], [4, 6], [6, 4], [8, 2]]
    ]
CLASS_PAGE = [
    "https://en.wikipedia.org/wiki/List_of_scientific_occupations", 
    "https://en.wikipedia.org/wiki/List_of_artistic_occupations"
    ]

@app.route("/questionnaire", methods=['GET'])
def get_questionnaire():
    return render_template('questionnaire.html')

@app.route("/result", methods=['GET'])
def get_result():
    i_question = 0
    personal_score = [0, 0]
    for question in request.args:
        for i in range(NUMBER_OF_CLASSES):
            personal_score[i] += WEIGHT_VECTORS[i_question][int(request.args.get(question))][i]
        i_question += 1
    return redirect(CLASS_PAGE[personal_score.index(max(personal_score))])

if __name__ == '__main__':
   app.run()