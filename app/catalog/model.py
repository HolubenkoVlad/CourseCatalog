from peewee import *

conn = SqliteDatabase('..\..\database\catalog.db')


class BaseModel(Model):
    class Meta:
        database = conn


class Course(BaseModel):
    id = AutoField(column_name='id')
    name = TextField(column_name='name', null=True)
    start_date = DateField(column_name='start_date', null=True)
    end_date = DateField(column_name='end_date', null=True)
    lectures_number = IntegerField(column_name='lectures_number', null=True)

    class Meta:
        table_name = 'Course'
