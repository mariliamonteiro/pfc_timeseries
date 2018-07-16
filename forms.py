from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import InputRequired

class FormARIMA(FlaskForm):
    p = IntegerField('P',default=1, validators= [InputRequired()])
    d = IntegerField('D',default=0, validators= [InputRequired()])
    q = IntegerField('Q',default=0, validators= [InputRequired()])

    submit = SubmitField('Processar')
