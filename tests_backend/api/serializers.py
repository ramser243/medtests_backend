from flask_restplus import fields
from tests_backend.api.restplus import api

themes = api.model('Themes', {
    'name': fields.String(required=True, description='Theme title'),
    'url': fields.String(required=False, description='Theme URL'),
    'open_counter': fields.Integer(required=False, description='Theme opened'),
})