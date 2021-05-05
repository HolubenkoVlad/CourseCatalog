from peewee import SQL
from app.catalog.model import Course
from playhouse.shortcuts import model_to_dict


def courses_list():
    courses = Course.select()
    courses_name_list = [model_to_dict(course) for course in courses]
    return courses_name_list


def course_by_id(course_id):
    try:
        course = Course.get_by_id(course_id)
    except Course.DoesNotExist:
        return None
    return model_to_dict(course)


def new_course(new_course_info):
    course = Course.get_by_id(Course.insert(new_course_info).execute())
    return model_to_dict(course)


def name():
    return "name LIKE ?"


def start_date():
    return "start_date >= ?"


def end_date():
    return "end_date <= ?"


table_attributes = {'name': name, 'start_date': start_date, 'end_date': end_date}


def courses_on_conditions(conditions):
    conditions_string = ""
    operator_flag = False
    if 'name' in conditions:
        conditions['name'] = '%{}%'.format(conditions['name'])
    # створюється список умов для того, щоб вводити параметри незалежно від їх кількості та порядку
    conditions_list = list()
    for key, value in conditions.items():
        conditions_list.append(value)
        if key in table_attributes.keys():
            if operator_flag:
                conditions_string += " AND "
            else:
                operator_flag = True
            conditions_string += table_attributes[key]()
    conditions_tuple = tuple(conditions_list)
    courses = Course.select().where(SQL(conditions_string, conditions_tuple))
    courses_name_list = [model_to_dict(course) for course in courses]
    return courses_name_list


def delete_course(course_id):
    return Course.delete_by_id(course_id)


def update_course(values, id_course):
    if Course.get_or_none(id=id_course) is not None:
        query = Course.update(values).where(Course.id == id_course)
        query.execute()
        return True
    else:
        return False
