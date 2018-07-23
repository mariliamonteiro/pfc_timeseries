from flask import Flask, render_template, url_for, redirect, request
from flask_uploads import UploadSet, configure_uploads, DATA, patch_request_class

from forms import *
from variables import *

import os
from werkzeug.utils import secure_filename
import pandas as pd
import secrets

from read_file import read_csv
from algo_acf import acf_plot, data_acf
from algo_pacf import pacf_plot, data_pacf
from algo_movingaverage import *
from algo_decomposition import *

# VARIAVEIS DE INICIALIZACAO ===================================================
app = Flask(__name__)

app.config['UPLOADED_FILES_DEST'] = 'temp_files'
app.config['UPLOAD_FOLDER'] = 'temp_files'

app.config['SECRET_KEY'] = 'd5fda74dcf2c2fdbfca06a4ebfc65b86a9e0da08d0115dce61f522f183b156d8'

files = UploadSet('files', DATA)
configure_uploads(app, files)
patch_request_class(app)

algos_list = shortDesc()
desc_list = longDesc()

# PAGINAS PRINCIPAIS ===========================================================
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/docs')
def about():
    return render_template('docs.html', title='Docs')

@app.route('/algorithms')
def algorithms():
    return render_template('algorithms.html', title= 'Algoritmos', algos_list= algos_list)

@app.route('/fileformats')
def fileformats():
    return render_template('file_formats.html', title= 'Formatos de Arquivos')

@app.route('/examples')
def examples():
    return render_template('examples.html', title= 'Exemplos')
# PAGINAS DE FORMULARIOS DOS ALGORITMOS UTILIZADOS =============================
@app.route('/algorithms/arima', methods= ['GET', 'POST'])
def algorithms_arima():
    text = desc_list['arima']

    form = FormARIMA()

    if form.validate_on_submit():
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        p = form.p.data
        q = form.q.data
        d = form.d.data
        result = (p, d, q, file_url)

        return render_template('algorithms_arima_output.html', title='ARIMA', text=text, form= form, file_url=file_url, result=result)
    else:
        file_url = None

    return render_template('algorithms_arima.html', title='ARIMA', text=text, form= form, file_url=file_url)

@app.route('/algorithms/acf', methods= ['GET', 'POST'])
def algorithms_acf():
    text = desc_list['acf']

    form = FormACF()

    if form.validate_on_submit():
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        lags = form.lags.data

        # Get data from file
        separator = form.sep.data
        header = form.header.data
        date_column = form.datec.data

        serie = read_csv(file_url, filename, separator, header, date_column)

        # Generate plot
        img_name = acf_plot(serie, lags)
        image_file = url_for('static', filename='images/'+ img_name)

        # Generate array of values
        acf_data = data_acf(serie, lags)

        return render_template('algorithms_acf_output.html', title='Função de Autocorrelação', text=text, form= form, file_url=file_url, lag=lags, image=image_file, data_acf=acf_data)

    else:
        file_url = None

    return render_template('algorithms_acf.html', title='Função de Autocorrelação', text=text, form= form, file_url=file_url)

@app.route('/algorithms/pacf', methods= ['GET', 'POST'])
def algorithms_pacf():
    text = desc_list['pacf']

    form = FormPACF()

    if form.validate_on_submit():
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        lags = form.lags.data

        # Get data from file
        separator = form.sep.data
        header = form.header.data
        date_column = form.datec.data

        serie = read_csv(file_url, filename, separator, header, date_column)

        # Generate plot
        img_name = pacf_plot(serie, lags)
        image_file = url_for('static', filename='images/'+ img_name)

        # Generate array of values
        pacf_data = data_pacf(serie, lags)

        return render_template('algorithms_pacf_output.html', title='Função de Autocorrelação Parcial', text=text, form= form, file_url=file_url, lag=lags, image=image_file, data_acf=pacf_data)

    else:
        file_url = None

    return render_template('algorithms_pacf.html', title='Função de Autocorrelação Parcial', text=text, form= form, file_url=file_url)

@app.route('/algorithms/movingaverage', methods= ['GET', 'POST'])
def algorithms_movingaverage():
    text = desc_list['movingaverage']

    form = FormMA()

    if form.validate_on_submit():
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        window = form.window.data

        # Get data from file
        separator = form.sep.data
        header = form.header.data
        date_column = form.datec.data

        serie = read_csv(file_url, filename, separator, header, date_column)

        # Generate plot
        img_name = ma_plot(serie, window)
        image_file = url_for('static', filename='images/'+ img_name)

        # Generate array of values
        ma_data = data_ma(serie, window)

        return render_template('algorithms_movingaverage_output.html', title='Média Móvel', text=text, form=form, file_url=file_url, window=window, image=image_file, data_ma=ma_data)

    else:
        file_url = None

    return render_template('algorithms_movingaverage.html', title='Função de Autocorrelação Parcial', text=text, form= form, file_url=file_url)

@app.route('/algorithms/decomposition', methods= ['GET', 'POST'])
def algorithms_decomposition():
    text = desc_list['decomposition']

    form = FormDecomposition()

    if form.validate_on_submit():
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        model = form.model.data

        # Get data from file
        separator = form.sep.data
        header = form.header.data
        date_column = form.datec.data

        serie = read_csv(file_url, filename, separator, header, date_column)

        # Generate plot
        img_name = decomposition_plot(serie, model)
        image_file = url_for('static', filename='images/'+ img_name)

        # Generate array of values


        return render_template('algorithms_decomposition_output.html', title='Decomposição de Séries', text=text, form=form, file_url=file_url, model=model, image=image_file)

    else:
        file_url = None

    return render_template('algorithms_decomposition.html', title='Decomposição de Séries', text=text, form= form, file_url=file_url)

# INICIAR SERVIDOR =============================================================
if __name__ == '__main__':
    app.run(debug= False)
