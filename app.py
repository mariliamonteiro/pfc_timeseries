from flask import Flask, render_template, url_for, redirect, request, send_from_directory
from flask_uploads import UploadSet, configure_uploads, DATA, patch_request_class

from forms import *
from variables import *

import os
from werkzeug.utils import secure_filename
import pandas as pd
import secrets

import matplotlib
matplotlib.use('agg')
from matplotlib.pylab import rcParams
rcParams['lines.linewidth'] = 0.5

from operations import deal_inputs, readdata_table, summary_maincol
from delete_images import *
from delete_reports import *
from report import *

from algos.acf import *
from algos.pacf import *
from algos.movingaverage import *
from algos.decomposition import *
from algos.periodogram import *
from algos.arima import *
from algos.diff import *

# VARIAVEIS DE INICIALIZACAO ===================================================
app = Flask(__name__)

app.config['SECRET_KEY'] = 'no-secret-but-should-be'

app.config['UPLOADED_FILES_DEST'] = 'temp_files'
app.config['UPLOAD_FOLDER'] = 'temp_files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

files = UploadSet('files', DATA)
configure_uploads(app, files)
patch_request_class(app)

algos_list = shortDesc()
desc_list = longDesc()
dict_lista = shortDescDicionario()
dias = 0.0005

# PAGINAS PRINCIPAIS ===========================================================
@app.route('/')
@app.route('/home')
def home():
    delete_images(dias)
    delete_reports(dias)
    return render_template('home.html', title = 'Home')

@app.route('/docs')
def about():
    return render_template('docs.html', title='Docs')

@app.route('/algorithms')
def algorithms():
    delete_images(dias)
    delete_reports(dias)
    return render_template('algorithms.html', title= 'Algoritmos', algos_list= algos_list)

@app.route('/fileformats')
def fileformats():
    return render_template('file_formats.html', title= 'Formatos de Arquivos')

@app.route('/examples')
def examples():
    return render_template('examples.html', title= 'Exemplos')

@app.route('/examples/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='toydata', filename=filename, as_attachment= True)

@app.route('/algorithms/<path:filename>', methods=['GET', 'POST'])
def download_acf(filename):
    return send_from_directory(directory='static/reports', filename=filename, as_attachment= True)

@app.errorhandler(403)
@app.errorhandler(413)
@app.errorhandler(500)
def page_error(e):
    return render_template('500.html', title = 'Erro na aplicação'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title = 'Página não encontrada', link= request.referrer), 404

# PAGINAS DE FORMULARIOS DOS ALGORITMOS UTILIZADOS =============================
@app.route('/algorithms/acf', methods= ['GET', 'POST'])
def algorithms_acf():
    text = desc_list['01acf']

    form = FormACF()

    if form.validate_on_submit():
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        lags = form.lags.data

        # Get data from file
        separator = form.sep.data
        serie, rd, quality_param = deal_inputs(file_url, filename, form, isseries= True)

        # Generate plot
        img_name = acf_plot(serie, lags)
        image_file = url_for('static', filename='images/'+ img_name)

        ### Create report

        # Report title
        title = dict_lista['01acf']['title']

        # Model parameters
        model_param = [['Lags', str(lags)]]
        readdata_param = readdata_table(form)
        summary_param = summary_maincol(serie)
        file_title = 'acf'
        address_pdf = create_report(title, model_param, readdata_param, quality_param, summary_param, [image_file], file_title)


        # Generate array of values
        acf_data, df_output = data_acf(serie, lags)

        # Create csv for downloading
        address_csv = '%s_%s.csv' % (file_title, secrets.token_hex(6))
        df_output.to_csv('static/reports/%s' % (address_csv), sep = separator, index = False, encoding='utf-8-sig')

        return render_template('algorithms_acf_output.html', title='Função de Autocorrelação', text=text, form= form, file_url=file_url, lag=lags, image=image_file, data_acf=acf_data, address_pdf = address_pdf, address_csv = address_csv)

    else:
        file_url = None

    return render_template('algorithms_acf.html', title='Função de Autocorrelação', text=text, form= form, file_url=file_url)

@app.route('/algorithms/pacf', methods= ['GET', 'POST'])
def algorithms_pacf():
    text = desc_list['02pacf']

    form = FormPACF()

    if form.validate_on_submit():
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        lags = form.lags.data

        # Get data from file
        separator = form.sep.data
        serie, rd, quality_param = deal_inputs(file_url, filename, form, isseries= True)

        # Generate plot
        img_name = pacf_plot(serie, lags)
        image_file = url_for('static', filename='images/'+ img_name)

        ### Create report

        # Report title
        title = dict_lista['02pacf']['title']

        # Model parameters
        model_param = [['Lags', str(lags)]]
        readdata_param = readdata_table(form)
        summary_param = summary_maincol(serie)
        file_title = 'pacf'
        address_pdf = create_report(title, model_param, readdata_param, quality_param, summary_param, [image_file], file_title)

        # Generate array of values
        pacf_data, df_output = data_pacf(serie, lags, rd)

        # Create csv for downloading
        address_csv = '%s_%s.csv' % (file_title, secrets.token_hex(6))
        df_output.to_csv('static/reports/%s' % (address_csv), sep = separator, index = False, encoding='utf-8-sig')

        return render_template('algorithms_pacf_output.html', title='Função de Autocorrelação Parcial', text=text, form= form, file_url=file_url, lag=lags, image=image_file, data_acf=pacf_data, address_pdf = address_pdf, address_csv = address_csv)

    else:
        file_url = None

    return render_template('algorithms_pacf.html', title='Função de Autocorrelação Parcial', text=text, form= form, file_url=file_url)

@app.route('/algorithms/decomposition', methods= ['GET', 'POST'])
def algorithms_decomposition():
    text = desc_list['03decomposition']

    form = FormDecomposition()

    if form.validate_on_submit():
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        model = form.model.data
        frequencia = form.sazon.data

        ts = form.reference.data
        if ts == 'center':
            two_sided = True
        elif ts == 'right':
            two_sided = False

        # Get data from file
        separator = form.sep.data
        serie, rd, quality_param = deal_inputs(file_url, filename, form, isseries= True)

        # Generate plot
        img_name = decomposition_plot(serie, model, frequencia, two_sided)
        image_file = url_for('static', filename='images/'+ img_name)

        ### Create report

        # Report title
        title = dict_lista['03decomposition']['title']

        # Model parameters
        model_param = [['Modelo', str(model)],
                       ['Referência da Média Móvel', str(ts)],
                       ['Periodicidade', str(frequencia)]]
        readdata_param = readdata_table(form)
        summary_param = summary_maincol(serie)
        file_title = 'decomposition'
        address_pdf = create_report(title, model_param, readdata_param, quality_param, summary_param, [image_file], file_title)


        # Generate array of values
        trend, seasonal, residual, df_output = data_decomposition(serie, model, frequencia, two_sided, rd)

        # Create csv for downloading
        address_csv = '%s_%s.csv' % (file_title, secrets.token_hex(6))
        df_output.to_csv('static/reports/%s' % (address_csv), sep = separator, index = False, encoding='utf-8-sig')

        return render_template('algorithms_decomposition_output.html', title='Decomposição de Séries', text=text, form=form, file_url=file_url, model=model, image=image_file, trend=trend, seasonal=seasonal, residual=residual, rd=rd, two_sided=ts, frequencia=frequencia, address_pdf = address_pdf, address_csv = address_csv)

    else:
        file_url = None

    return render_template('algorithms_decomposition.html', title='Decomposição de Séries', text=text, form= form, file_url=file_url)

@app.route('/algorithms/movingaverage', methods= ['GET', 'POST'])
def algorithms_movingaverage():
    text = desc_list['04movingaverage']

    form = FormMA()

    if form.validate_on_submit() and request.method == 'POST':
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        window = form.window.data

        # Get data from file
        separator = form.sep.data
        serie, rd, quality_param = deal_inputs(file_url, filename, form, isseries= True)

        # Generate plot
        img_name = ma_plot(serie, window)
        image_file = url_for('static', filename='images/'+ img_name)

        ### Create report

        # Report title
        title = dict_lista['04movingaverage']['title']

        # Model parameters
        model_param = [['Janela', str(window)]]
        readdata_param = readdata_table(form)
        summary_param = summary_maincol(serie)
        file_title = 'movingaverage'
        address_pdf = create_report(title, model_param, readdata_param, quality_param, summary_param, [image_file], file_title)

        # Generate array of values
        ma_data, df_output = data_ma(serie, window, rd)

        # Create csv for downloading
        address_csv = '%s_%s.csv' % (file_title, secrets.token_hex(6))
        df_output.to_csv('static/reports/%s' % (address_csv), sep = separator, index = False, encoding='utf-8-sig')

        return render_template('algorithms_movingaverage_output.html', title='Média Móvel', text=text, form=form, file_url=file_url, window=window, image=image_file, data_ma=ma_data, raw_data=rd, address_pdf = address_pdf, address_csv = address_csv)

    else:
        file_url = None

    return render_template('algorithms_movingaverage.html', title='Média Móvel', text=text, form= form, file_url=file_url)

@app.route('/algorithms/periodogram', methods= ['GET', 'POST'])
def algorithms_periodogram():
    text = desc_list['05periodogram']

    form = FormPeriodogram()

    if form.validate_on_submit() and request.method == 'POST':
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form


        # Get data from file
        separator = form.sep.data
        serie, rd, quality_param = deal_inputs(file_url, filename, form, isseries= True)

        # Generate plot
        img_name = periodogram_plot(serie)

        image_file = url_for('static', filename='images/'+ img_name)

        ### Create report

        # Report title
        title = dict_lista['05periodogram']['title']

        # Model parameters
        model_param = [['Não há parâmetros no método','-']]
        readdata_param = readdata_table(form)
        summary_param = summary_maincol(serie)
        file_title = 'periodogram'
        address_pdf = create_report(title, model_param, readdata_param, quality_param, summary_param, [image_file], file_title)

        # Generate array of values
        periodogram_data, freq, df_output, index, freq_max = data_periodogram(serie)

        T = len(serie)/index

        # Create csv for downloading
        address_csv = '%s_%s.csv' % (file_title, secrets.token_hex(6))
        df_output.to_csv('static/reports/%s' % (address_csv), sep = separator, index = False)

        return render_template('algorithms_periodogram_output.html', title='Periodograma', text=text, form=form, file_url=file_url, image=image_file, data_periodogram=periodogram_data, address_pdf = address_pdf, address_csv = address_csv, periodo=T, index=index, freq_max=freq_max)

    else:
        file_url = None

    return render_template('algorithms_periodogram.html', title='Periodograma', text=text, form= form, file_url=file_url)

@app.route('/algorithms/arima', methods= ['GET', 'POST'])
def algorithms_arima():
    text = desc_list['06arima']

    form = FormARIMA()

    if form.validate_on_submit():
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        p = form.p.data
        q = form.q.data
        d = form.d.data
        ptest = form.percent_test.data
        predict_range = form.predict_range.data

        # Get data from file
        separator = form.sep.data
        serie, rd, quality_param = deal_inputs(file_url, filename, form, isseries= True)

        # Generate plot
        elementos, img_name_residuo, img_name_hist, img_name_forecast = fit_arima(serie, p, d, q, ptest)
        img_name_predict = predict_arima(serie, p, d, q, predict_range)

        image_file_residuo = url_for('static', filename='images/'+ img_name_residuo)
        image_file_hist = url_for('static', filename='images/'+ img_name_hist)
        image_file_forecast = url_for('static', filename='images/'+ img_name_forecast)
        image_file_predict = url_for('static', filename='images/'+ img_name_predict)

        ### Create report

        # Report title
        title = dict_lista['06arima']['title']

        # Model parameters
        model_param = [['p', str(p)],
                       ['d', str(d)],
                       ['q', str(q)],
                       ]
        readdata_param = readdata_table(form)
        summary_param = summary_maincol(serie)
        file_title = 'arima'
        address_pdf = create_report_arima(title, model_param, readdata_param, quality_param, summary_param, [image_file_residuo, image_file_hist, image_file_forecast, image_file_predict], file_title, elementos)


        # Generate array of values

        # Create csv for downloading
        address_csv = '%s_%s.csv' % (file_title, secrets.token_hex(6))
        #df_output.to_csv('static/reports/%s' % (address_csv), sep = separator, index = False, encoding='utf-8-sig')

        return render_template('algorithms_arima_output.html', title='ARIMA', text=text, form=form, file_url=file_url, p = p, q=q, d=d, listap = list(range(p)), listaq = list(range(q)), ptest=ptest, range=predict_range, image_residuo = image_file_residuo, image_hist = image_file_hist, image_forecast=image_file_forecast, image_predict = image_file_predict, rd=rd, address_pdf = address_pdf, address_csv = address_csv, result_data = elementos)

    else:
        file_url = None

    return render_template('algorithms_arima.html', title='ARIMA', text=text, form= form, file_url=file_url)

@app.route('/algorithms/diff', methods= ['GET', 'POST'])
def algorithms_diff():
    text = desc_list['07diff']

    form = FormDiff()

    if form.validate_on_submit() and request.method == 'POST':
        filename = secrets.token_hex(8) + '.csv'
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(filename)

        # Retrieving results from the form
        order = form.diff.data

        # Get data from file
        separator = form.sep.data
        serie, rd, quality_param = deal_inputs(file_url, filename, form, isseries= True)

        # Generate plot and array of values
        img_name, diff_data, df_output = diff(serie, order, rd)
        image_file = url_for('static', filename='images/'+ img_name)

        ### Create report

        # Report title
        title = dict_lista['07diff']['title']

        # Model parameters
        model_param = [['Ordem', str(order)]]
        readdata_param = readdata_table(form)
        summary_param = summary_maincol(serie)
        file_title = 'diff'
        address_pdf = create_report(title, model_param, readdata_param, quality_param, summary_param, [image_file], file_title)

        # Create csv for downloading
        address_csv = '%s_%s.csv' % (file_title, secrets.token_hex(6))
        df_output.to_csv('static/reports/%s' % (address_csv), sep = separator, index = False, encoding='utf-8-sig')

        return render_template('algorithms_diff_output.html', title='Diferença', text=text, form=form, file_url=file_url, order=order, image=image_file, data_diff=diff_data, raw_data=rd, address_pdf = address_pdf, address_csv = address_csv)

    else:
        file_url = None

    return render_template('algorithms_diff.html', title='Diferença', text=text, form= form, file_url=file_url)

# INICIAR SERVIDOR =============================================================
if __name__ == '__main__':
    app.run(debug= False)
