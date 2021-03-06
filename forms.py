from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FloatField
from wtforms.validators import InputRequired, Length
from wtforms import SubmitField

# == CAMPOS DE UPLOAD FIXOS PARA TODOS OS FORMULÁRIOS ====

class UploadGlobal(FlaskForm):
    dados = FileField('Dados*', validators=[FileAllowed(['csv'], 'Somente arquivos .csv'), FileRequired()])
    sep = StringField('Separador*', default=',', validators=[Length(min=1, max=2), InputRequired()])
    header = BooleanField('Cabeçalho*', default= True)
    datec = IntegerField('Coluna de datas', default= 1)
    datac = IntegerField('Coluna principal', default= 2)
    missing = SelectField('Tratamento de Dados Faltantes', choices=[('drop','Remoção'),('ffill','Forward Fill'),('linear','Interpolação Linear'),('cubic','Interpolação Cúbica')], validators= [InputRequired()], default='drop')
    freq = SelectField('Frequência dos Dados', choices=[('H','Hora em hora'),('D','Diária'),('W','Semanal'),('SMS','Quinzenal'),('MS','Mensal'),('QS','Trimestral'),('YS','Anual')], validators= [InputRequired()], default='MS')

    submit = SubmitField('Processar')

# == CAMPOS ESPECÍFICOS DE CADA ALGORITMO ====

# Autocorrelação total
class FormACF(UploadGlobal):
    lags = IntegerField('Lags*',default=20, validators= [InputRequired()])

# Autocorrelação parcial
class FormPACF(UploadGlobal):
    lags = IntegerField('Lags',default=20, validators= [InputRequired()])

# Média móvel
class FormMA(UploadGlobal):
    window = IntegerField('Janela',default=12, validators= [InputRequired()])

# Decomposição clássica de séries temporais
class FormDecomposition(UploadGlobal):
    model = SelectField('Modelo', choices=[('additive','Aditivo'),('multiplicative','Multiplicativo')], validators= [InputRequired()])
    reference = SelectField('Referência Média Móvel', choices=[('center', 'Centrada'), ('right', 'À direita')], validators= [InputRequired()], default='right')

    sazon = IntegerField('Sazonalidade dos Dados', default=12)

# Periodograma
class FormPeriodogram(UploadGlobal):
    _ignore = 0

# ARIMA
class FormARIMA(UploadGlobal):
    p = IntegerField('p',default=1, validators= [InputRequired()])
    q = IntegerField('q',default=1, validators= [InputRequired()])
    d = IntegerField('d',default=1, validators= [InputRequired()])
    percent_test = FloatField('Teste (%)',default=10, validators= [InputRequired()])
    predict_range = IntegerField('Intervalo de Predição',default=10, validators= [InputRequired()])

class FormDiff(UploadGlobal):
    diff = IntegerField('Ordem',default=1, validators= [InputRequired()])

# SARIMA
class FormSARIMA(UploadGlobal):
    p = IntegerField('p',default=1, validators= [InputRequired()])
    q = IntegerField('q',default=1, validators= [InputRequired()])
    d = IntegerField('d',default=1, validators= [InputRequired()])
    P = IntegerField('P',default=1, validators= [InputRequired()])
    D = IntegerField('D',default=1, validators= [InputRequired()])
    Q = IntegerField('Q',default=1, validators= [InputRequired()])
    sazon = IntegerField('Sazonalidade',default=12, validators= [InputRequired()])
    percent_test = FloatField('Teste (%)',default=10, validators= [InputRequired()])
    predict_range = IntegerField('Intervalo de Predição',default=10, validators= [InputRequired()])
