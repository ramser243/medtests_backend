import logging

from flask_restplus import Resource
from tests_backend.api.serializers import themes
from tests_backend.api.restplus import api
from flask import request, current_app

log = logging.getLogger(__name__)

admin_route = api.namespace('admin', description='admin operations')


@admin_route.route('/')
class AdminLogin(Resource):

    def post(self):
        if 'login' in request.json and 'password' in request.json:
            if request.json['login'] == current_app.config['ADMIN_LOGIN'] and request.json['password'] == current_app.config['ADMIN_PASSWORD']:
                return {}, 200
        return {}, 401