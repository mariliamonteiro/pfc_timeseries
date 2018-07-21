from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import InputRequired
from wtforms import SubmitField

class FormARIMA(FlaskForm):
    p = IntegerField('P',default=1, validators= [InputRequired()])
    d = IntegerField('D',default=0, validators= [InputRequired()])
    q = IntegerField('Q',default=0, validators= [InputRequired()])

    dados = FileField('Dados', validators=[FileAllowed(['csv'], 'Somente arquivos .csv'), FileRequired()])

    submit = SubmitField('Processar')
