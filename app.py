import os
from flask import Flask, render_template, url_for, redirect, request
from flask_uploads import UploadSet, configure_uploads, DATA, patch_request_class
from forms import *
from variables import *
from werkzeug.utils import secure_filename
from algo_readfile import extractSerie
from algo_acf import acf_plot, data_acf

# VARIAVEIS DE INICIALIZACAO ===================================================
app = Flask(__name__)
desc_list = longDesc()

app.config['SECRET_KEY'] = 'd5fda74dcf2c2fdbfca06a4ebfc65b86a9e0da08d0115dce61f522f183b156d8'
app.config['UPLOADED_FILES_DEST'] = 'temp_files'

files = UploadSet('files', DATA)
configure_uploads(app, files)
patch_request_class(app)

UPLOAD_FOLDER = 'temp_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

# PAGINAS DE FORMULARIOS DOS ALGORITMOS UTILIZADOS =============================
@app.route('/algorithms/arima', methods= ['GET', 'POST'])
def algorithms_arima():
    text = desc_list['arima']

    form = FormARIMA()

    if form.validate_on_submit():
        filename = secure_filename(form.dados.data.filename)
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(form.dados.data.filename)

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
        filename = secure_filename(form.dados.data.filename)
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = files.url(form.dados.data.filename)

        # Retrieving results from the form
        lags = form.lags.data

        # Get data from file
        serie = extractSerie(file_url)

        # Generate plot
        img_name = acf_plot(serie, lags)
        image_file = url_for('static', filename='images/'+ img_name)

        # Generate array of values
        acf_data = data_acf(serie, lags)

        return render_template('algorithms_acf_output.html', title='Função de Autocorrelação', text=text, form= form, file_url=file_url, lag=lags, image=image_file, data_acf=acf_data)
    else:
        file_url = None

    return render_template('algorithms_acf.html', title='Função de Autocorrelação', text=text, form= form, file_url=file_url)

# INICIAR SERVIDOR =============================================================
if __name__ == '__main__':
    app.run(debug= True)
