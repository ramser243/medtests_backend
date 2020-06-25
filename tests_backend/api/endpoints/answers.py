import logging

from flask import request
from flask_restplus import Resource
from tests_backend.api.restplus import api
from tests_backend.models import Answer

log = logging.getLogger(__name__)

answers_route = api.namespace('answers', description='answers operations')


@answers_route.route('/<int:answer_id>')
@api.response(404, 'Answer not found.')
class AnswerItem(Resource):

    def post(self, answer_id):
        if 'admin' in request.json and 'name' in request.json and 'value' in request.json:
            if request.json['admin'] == 'true':
                answer = Answer.query.filter(Answer.id == answer_id).one()
                answer.name = request.json['name']
                answer.value = request.json['value']
                answer.save()
                return 200