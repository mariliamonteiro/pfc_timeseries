from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length
from wtforms import SubmitField

class FormARIMA(FlaskForm):
    p = IntegerField('P',default=1, validators= [InputRequired()])
    d = IntegerField('D',default=0, validators= [InputRequired()])
    q = IntegerField('Q',default=0, validators= [InputRequired()])

    dados = FileField('Dados', validators=[FileAllowed(['csv'], 'Somente arquivos .csv'), FileRequired()])

    submit = SubmitField('Processar')

class FormACF(FlaskForm):
    lags = IntegerField('Lags*',default=1, validators= [InputRequired()])

    # CAMPOS FIXOS PARA TODOS OS FORMULÁRIOS (ARQUIVO)
    dados = FileField('Dados*', validators=[FileAllowed(['csv'], 'Somente arquivos .csv'), FileRequired()])
    sep = StringField('Separador*', default=',', validators=[Length(min=1, max=2), InputRequired()])
    header = BooleanField('Cabeçalho*', default= True)
    datec = IntegerField('Coluna de datas')

    submit = SubmitField('Processar')

class FormPACF(FlaskForm):
    lags = IntegerField('Lags',default=1, validators= [InputRequired()])

    # CAMPOS FIXOS PARA TODOS OS FORMULÁRIOS (ARQUIVO)
    dados = FileField('Dados', validators=[FileAllowed(['csv'], 'Somente arquivos .csv'), FileRequired()])
    sep = StringField('Separador', default=',', validators=[Length(min=1, max=2), InputRequired()])
    header = BooleanField('Cabeçalho', default= True)
    datec = IntegerField('Coluna de datas')

    submit = SubmitField('Processar')
