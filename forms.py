from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length
from wtforms import SubmitField

class FormACF(FlaskForm):
    lags = IntegerField('Lags*',default=20, validators= [InputRequired()])

    # CAMPOS FIXOS PARA TODOS OS FORMULÁRIOS (ARQUIVO)
    dados = FileField('Dados*', validators=[FileAllowed(['csv'], 'Somente arquivos .csv'), FileRequired()])
    sep = StringField('Separador*', default=',', validators=[Length(min=1, max=2), InputRequired()])
    header = BooleanField('Cabeçalho*', default= True)
    datec = IntegerField('Coluna de datas', default= 1)
    datac = IntegerField('Coluna principal', default= 2)

    submit = SubmitField('Processar')

class FormPACF(FlaskForm):
    lags = IntegerField('Lags',default=20, validators= [InputRequired()])

    # CAMPOS FIXOS PARA TODOS OS FORMULÁRIOS (ARQUIVO)
    dados = FileField('Dados', validators=[FileAllowed(['csv'], 'Somente arquivos .csv'), FileRequired()])
    sep = StringField('Separador', default=',', validators=[Length(min=1, max=2), InputRequired()])
    header = BooleanField('Cabeçalho', default= True)
    datec = IntegerField('Coluna de datas', default= 1)
    datac = IntegerField('Coluna principal', default= 2)

    submit = SubmitField('Processar')

class FormMA(FlaskForm):
    window = IntegerField('Janela',default=3, validators= [InputRequired()])

    # CAMPOS FIXOS PARA TODOS OS FORMULÁRIOS (ARQUIVO)
    dados = FileField('Dados', validators=[FileAllowed(['csv'], 'Somente arquivos .csv'), FileRequired()])
    sep = StringField('Separador', default=',', validators=[Length(min=1, max=2), InputRequired()])
    header = BooleanField('Cabeçalho', default= True)
    datec = IntegerField('Coluna de datas', default= 1)
    datac = IntegerField('Coluna principal', default= 2)

    submit = SubmitField('Processar')

class FormDecomposition(FlaskForm):
    model = SelectField('Modelo', choices=[('adictive','Aditivo'),('multiplicative','Multiplicativo')], validators= [InputRequired()])

    # CAMPOS FIXOS PARA TODOS OS FORMULÁRIOS (ARQUIVO)
    dados = FileField('Dados', validators=[FileAllowed(['csv'], 'Somente arquivos .csv'), FileRequired()])
    sep = StringField('Separador', default=',', validators=[Length(min=1, max=2), InputRequired()])
    header = BooleanField('Cabeçalho', default= True)
    datec = IntegerField('Coluna de datas', default= 1)
    datac = IntegerField('Coluna principal', default= 2)

    submit = SubmitField('Processar')
