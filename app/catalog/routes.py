import datetime

from flask import Blueprint, request, Response, jsonify, abort
from flask_marshmallow import Schema
from marshmallow import fields, EXCLUDE, ValidationError
from marshmallow.validate import Range

from app.catalog.queries import *
import json

catalog = Blueprint('catalog', __name__)


# errorhandler, що викликається, якщо курс не знайдено в базі даних
@catalog.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


# errorhandler, що викликається, якщо користувач неправильно ввів аргументи, або взагалі нічого не ввів
@catalog.errorhandler(422)
def wrong_arguments(errors):
    error_list = list()
    for key, value in errors.description.items():
        error_list.append({"field": key, "reason": value})
    error_dict = {"errors": error_list}
    return Response(json.dumps(error_dict), status=422, mimetype='application/json')


@catalog.route('/course/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    course = course_by_id(course_id)
    course_dict = dict()
    if course is None:
        abort(404, description="Course not found")
    else:
        course_dict = {'course': course}
    return jsonify(course_dict)


# схема для контролю правильності введення аргументів для методу POST
class PostInputSchema(Schema):
    name = fields.String(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    lectures_number = fields.Integer(required=True, validate=Range(min=1))

    class Meta:
        unknown = EXCLUDE


@catalog.route('/new/course/', methods=['POST'])
def add_new_course():
    values = {}
    try:
        values = PostInputSchema().load(request.get_json())
    except ValidationError as err:
        abort(422, err.args[0])
    course = new_course(values)
    return jsonify({"course": course}), 201


# схема для контролю правильності введення аргументів для методу GET
class GetInputSchema(Schema):
    name = fields.String()
    start_date = fields.Date()
    end_date = fields.Date()

    class Meta:
        unknown = EXCLUDE


def date_converter(o):
    if isinstance(o, datetime.date):
        return o.__str__()


@catalog.route('/courses/', methods=['GET'])
def get_filtered_course_list():
    conditions = {}
    if request.get_json() is not None:
        try:
            conditions = GetInputSchema().load(request.get_json())
        except ValidationError as err:
            abort(422, err.args[0])
    list_of_courses = []
    if len(conditions) == 0:
        list_of_courses = {'courses': courses_list()}
    else:
        list_of_courses = {'courses': courses_on_conditions(conditions)}
    return Response(json.dumps(list_of_courses, default=date_converter), mimetype='application/json')


@catalog.route('/delete/course/<int:course_id>', methods=['DELETE'])
def delete_course_by_id(course_id):
    temp = delete_course(course_id)
    if not temp:
        return Response(json.dumps({"error": {"message": "Course doesn't exist"}}), status=404,
                        mimetype='application/json')
    return Response(json.dumps({"message": "The course has been deleted"}), status=200, mimetype='application/json')


# схема для контролю правильності введення аргументів для методу UPDATE
class UpdateInputSchema(Schema):
    name = fields.String()
    start_date = fields.Date()
    end_date = fields.Date()
    lectures_number = fields.Integer(validate=Range(min=1))

    class Meta:
        unknown = EXCLUDE


# вказується id курсу за яким буде проводитися оновлення даних. Дані для оновлення передаються у форматі json
@catalog.route('/update/course/<int:course_id>', methods=['PUT'])
def update_course_by_column(course_id):
    values = {}
    try:
        values = UpdateInputSchema().load(request.get_json())
    except ValidationError as err:
        abort(422, err.args[0])
    if len(values) == 0:
        abort(422, {"arguments": "are missing"})
    update_result = update_course(values, course_id)
    if update_result:
        return Response(json.dumps({"message": "Data has been updated"}), status=200, mimetype='application/json')
    else:
        abort(404, "Course doesn't exist")
