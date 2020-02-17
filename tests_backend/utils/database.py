# -*- coding: utf-8 -*-
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
from .compat import basestring
from tests_backend.extensions import db
import decimal, datetime, json, random

migrate = Migrate()
Column = db.Column
relationship = relationship
Model = db.Model

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


class JsonModel(object):
    def as_dict_glob(self):
        d = {}
        for column in self.__table__.columns:
            if column.name not in ['created_at', 'updated_at']:
                d[column.name] = str(getattr(self, column.name))
        return d

    def object_as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def object_as_dict_with_keys(self, keys):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs if c.key in keys}

    def to_json(self):
        return json.dumps(self.object_as_dict(), default=alchemyencoder)

    def to_json_pretty(self):
        return "<br />".join(json.dumps(self.object_as_dict(),indent=True,sort_keys=True,default=alchemyencoder).split("\n"))

    def from_json(self, fields, j):
        [self.__setattr__(f, j.get(f, None)) for f in fields]
        return self

class ModelGetByIdMixin(object):
    @classmethod
    def get_by_id(cls, id):
        if any(
                (isinstance(id, basestring) and id.isdigit(),
                 isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None

    @classmethod
    def get_by_id_or_404(cls, id, project=None):
        if any(
                (isinstance(id, basestring) and id.isdigit(),
                 isinstance(id, (int, float))),
        ):
            res = cls.query.get(int(id))
            if res is not None:
                return res
            return None

def ReferenceCol(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = ReferenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
        nullable=nullable, **kwargs)


class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` \
        to any declarative-mapped class.
    """

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    __abstract__ = True
    all_model_watch_registry = set()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    @classmethod
    def check_fields(cls, income_dict):
        diff = set(income_dict.keys()) - set(cls.get_model_dict().keys())
        if len(diff):
            wrong_field = ', '.join(str(e) for e in diff)
            return {"error": "Wrong field detected", "field": wrong_field}
        for key, value in income_dict.items():
            setattr(cls, key, value)
        return cls

    @classmethod
    def get_model_dict(cls):
        return dict((column.name, getattr(cls, column.name))
                    for column in cls.__table__.columns)


class Timestamps(object):
    """
    Useful mixin to add generic timestamps.
    Recommended to use on most of the models.
    """
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
