import datetime as dt
from sqlalchemy.orm import relationship, backref
from tests_backend.utils.database import Column, Model, SurrogatePK, reference_col, relationship, ReferenceCol, JsonModel, \
    db, ModelGetByIdMixin, Timestamps, Model
from flask import current_app
import random
from sqlalchemy.sql import func

class Theme(Model, ModelGetByIdMixin, SurrogatePK, Timestamps, JsonModel):
    __tablename__ = 'themes'

    name = db.Column(db.String())
    url = db.Column(db.String())
    open_counter = db.Column(db.Integer(), default=0)

    def as_dict(self):
        item = self.as_dict_glob()
        item['questions'] = [q.as_dict() for q in self.questions]
        item['questions_amount'] = self.questions_amount()
        return item



    def questions_amount(self):
        return len(self.questions)

    def __repr__(self):
        return '<Theme %r>' % (self.name)


class Question(Model, ModelGetByIdMixin, SurrogatePK, Timestamps, JsonModel):
    __tablename__ = 'questions'

    name = db.Column(db.String())
    answered = db.Column(db.Integer(), default=0)
    in_theme_id = db.Column(db.Integer(), default=0)
    answered_correct = db.Column(db.Integer(), default=0)
    theme_id = ReferenceCol('themes', index=True, nullable=False)
    theme = relationship('Theme', backref=backref("questions"))

    def as_dict(self):
        item = self.as_dict_glob()
        item['answers'] = [a.as_dict_glob() for a in self.answers]
        item['answers_amount'] = self.answers_amount()
        item['theme_title'] = self.theme.name

        return item

    @classmethod
    def select_for_exam(cls, theme_id, num_questions=30):
        res = cls.query.filter(cls.theme_id == theme_id).order_by(func.random()).limit(num_questions).all()
        result = []
        for i in res:
            result.append(i.as_dict())
        return result

    def answers_amount(self):
        return len(self.answers)

    def __repr__(self):
        return '<Question %r>' % (self.name)


class Answer(Model, ModelGetByIdMixin, SurrogatePK, Timestamps, JsonModel):
    __tablename__ = 'answers'

    name = db.Column(db.String())
    value = db.Column(db.Integer())
    in_question_id = db.Column(db.Integer(), default=0)
    question_id = ReferenceCol('questions', index=True, nullable=False)
    question = relationship('Question', backref=backref("answers"))

    def __repr__(self):
        return '<Question %r>' % (self.name)


class Comment(Model, ModelGetByIdMixin, SurrogatePK, Timestamps, JsonModel):
    __tablename__ = 'comments'

    author = db.Column(db.String())
    comment = db.Column(db.String())
    email_sent = db.Column(db.DateTime())
    question_id = ReferenceCol('questions', index=True, nullable=False)
    question = relationship('Question', backref=backref("comments"))

    def __repr__(self):
        return '<Comment %r>' % (self.comment)
