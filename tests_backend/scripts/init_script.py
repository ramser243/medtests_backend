from tests_backend.models.models import *
from flask import current_app
from tests_backend.utils.database import db
from tests_backend.scripts import tests_to_json


def generate_data():
    db.session.query(Theme).delete()
    db.session.query(Question).delete()
    db.session.query(Answer).delete()
    db.session.query(Comment).delete()

    themes_list = tests_to_json.grab_tests()

    for theme in themes_list:
        theme_db = Theme(name=theme['name'], url=theme['url'])
        theme_db.save()
        in_theme_id = 0
        for question in theme['questions']:
            in_theme_id = in_theme_id + 1
            question_db = Question(name=question, in_theme_id=in_theme_id)
            in_question_id = 0
            for answer in theme['questions'][question]:
                in_question_id = in_question_id + 1
                answer_db = Answer(name=answer, value=theme['questions'][question][answer], in_question_id=in_question_id)
                question_db.answers.append(answer_db)
            theme_db.questions.append(question_db)
        theme_db.save()

def init_data():
    with current_app.app_context():
        generate_data()
