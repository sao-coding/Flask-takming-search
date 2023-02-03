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

# FIXME:修改學生資料非必填

class CreateStudentForm(FlaskForm):
    country = SelectField('國家', choices=category_options)
    room = StringField('房間', validators=[DataRequired()])
    bed = StringField('床位', validators=[DataRequired()])
    member_class = StringField('班級', validators=[DataRequired()])
    student_ID = StringField('學號', validators=[DataRequired()])
    name = StringField('姓名', validators=[DataRequired()])
    ID_number = StringField('身分證字號', validators=[DataRequired()])
    birthday = DateField('生日', validators=[DataRequired()])
    phone = StringField('電話', validators=[DataRequired()])
    home_phone = StringField('家裡電話', validators=[DataRequired()])
    address = StringField('地址', validators=[DataRequired()])
    emergency_contact = StringField('緊急聯絡人', validators=[DataRequired()])
    emergency_contact_phone = StringField('緊急聯絡人電話', validators=[DataRequired()])
    submit = SubmitField('建立資料')

class EditStudentForm(FlaskForm):
    country = SelectField('國家', choices=category_options)
    room = StringField('房間', validators=[DataRequired()])
    bed = StringField('床位', validators=[DataRequired()])
    member_class = StringField('班級', validators=[DataRequired()])
    student_ID = StringField('學號', validators=[DataRequired()])
    name = StringField('姓名', validators=[DataRequired()])
    ID_number = StringField('身分證字號', validators=[DataRequired()])
    birthday = DateField('生日', validators=[DataRequired()])
    phone = StringField('電話', validators=[DataRequired()])
    home_phone = StringField('家裡電話', validators=[DataRequired()])
    address = StringField('地址', validators=[DataRequired()])
    emergency_contact = StringField('緊急聯絡人', validators=[DataRequired()])
    emergency_contact_phone = StringField('緊急聯絡人電話', validators=[DataRequired()])
    submit = SubmitField('更新資料')

class SearchStudentForm(FlaskForm):
    room = StringField('房間', validators=[DataRequired()])