import logging

from sqlalchemy import and_
from flask_restplus import Resource
from tests_backend.api.serializers import themes
from tests_backend.api.restplus import api
from tests_backend.models import Theme, Question, Answer

log = logging.getLogger(__name__)

themes_route = api.namespace('themes', description='themes operations')


@themes_route.route('/')
class ThemesCollection(Resource):

    @api.marshal_list_with(themes)
    def get(self):
        themes = Theme.query.all()
        return themes


@themes_route.route('/<int:theme_id>')
@api.response(404, 'Theme not found.')
class ThemeItem(Resource):

    def get(self, theme_id):
        theme = Theme.query.filter(Theme.id == theme_id).one()
        return theme.as_dict()


@themes_route.route('/exam/<int:theme_id>')
@api.response(404, 'Theme not found.')
class ExamQuestions(Resource):

    def get(self, theme_id):
        theme_res = Theme.query.filter(Theme.id == theme_id).first()
        theme = theme_res.as_dict()
        questions = Question.select_for_exam(theme_id)
        theme['questions'] = questions
        theme['questions_amount'] = 30
        return theme


@themes_route.route('/<int:theme_id>/questions')
class QuestionsCollection(Resource):

    def get(self, theme_id):
        theme = Theme.query.filter(Theme.id == theme_id).one()
        return [q.as_dict_glob() for q in theme.questions]


@themes_route.route('/<int:theme_id>/questions/<int:question_id>')
class QuestionItem(Resource):

    def get(self, theme_id, question_id):
        question = Question.query.filter(and_(Question.theme_id == theme_id),
                                          (Question.in_theme_id == question_id)).one()
        return question.as_dict()


@themes_route.route('/<int:theme_id>/questions/<int:question_id>/answers')
class AnswersCollection(Resource):

    def get(self, theme_id, question_id):
        question = Question.query.filter(and_(Question.theme_id == theme_id),
                                          (Question.in_theme_id == question_id)).one()
        return [a.as_dict_glob() for a in question.answers]


@themes_route.route('/<int:theme_id>/questions/<int:question_id>/answers/<int:answer_id>')
class AnswerItem(Resource):

    def get(self, theme_id, question_id, answer_id):
        db_question = Question.query.filter(and_(Question.theme_id == theme_id), (Question.id == question_id)).one()
        answer = Answer.query.filter(and_(Answer.question_id == db_question.id),
                                          (Answer.in_question_id == answer_id)).one()
        return answer.as_dict_glob()