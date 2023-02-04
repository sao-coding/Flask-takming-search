"Flask"
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, NumberRange

category_options = [
    ('台灣', '台灣'),
    ('日本', '日本'),
    ('香港', '香港'),
    ('越南', '越南'),
    ('其他', '其他')
]

class CreateStudentForm(FlaskForm):
    country = SelectField('國家', choices=category_options)
    room = StringField('房間', validators=[DataRequired()])
    bed = StringField('床位', validators=[DataRequired()])
    member_class = StringField('班級')
    student_ID = StringField('學號')
    name = StringField('姓名')
    ID_number = StringField('身分證字號')
    birthday = DateField('生日')
    phone = StringField('電話')
    home_phone = StringField('家裡電話')
    address = StringField('地址')
    emergency_contact = StringField('緊急聯絡人')
    emergency_contact_phone = StringField('緊急聯絡人電話')
    submit = SubmitField('建立資料')

class EditStudentForm(FlaskForm):
    country = SelectField('國家', choices=category_options)
    room = StringField('房間', validators=[DataRequired()])
    bed = StringField('床位', validators=[DataRequired()])
    member_class = StringField('班級')
    student_ID = StringField('學號')
    name = StringField('姓名')
    ID_number = StringField('身分證字號')
    birthday = DateField('生日')
    phone = StringField('電話')
    home_phone = StringField('家裡電話')
    address = StringField('地址')
    emergency_contact = StringField('緊急聯絡人')
    emergency_contact_phone = StringField('緊急聯絡人電話')
    submit = SubmitField('更新資料')

class SearchStudentForm(FlaskForm):
    room = StringField('房間', validators=[DataRequired()])