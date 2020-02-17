import logging

from flask import request
from flask_restplus import Resource
from tests_backend.api.serializers import themes
from tests_backend.api.restplus import api
from tests_backend.models import Question, Theme
from flask_mail import Message
from flask import current_app
from tests_backend.extensions import mail

log = logging.getLogger(__name__)

questions_route = api.namespace('questions', description='themes operations')


@questions_route.route('/<int:question_id>')
@api.response(404, 'Question not found.')
class QuestionItem(Resource):

    def get(self, question_id):
        question = Question.query.filter(Question.id == question_id).one()
        return question.as_dict()


@questions_route.route('/abuse')
class QuestionItemAbuse(Resource):

    def post(self):
        # mail_body = request.response['message']
        theme_title = request.json['theme']
        question_title = request.json['question']
        url = request.json['url']
        message = request.json['message']
        user_email = request.json['user_email']
        body = 'Тема: {0}\n\nВопрос: {1}\n\nURL: {2}\n\nСообщение: {3}\n\nUser Email: {4}'.\
            format(theme_title, question_title, url, message, user_email)
        msg = Message(subject="Отзыв о тестовом контроле",
                      sender=current_app.config['MAIL_USERNAME'],
                      recipients=['reanimatolog@bk.ru', 'ramser243@gmail.com'],  # replace with your email for testing
                      body=body)
        mail.send(msg)

        return 200