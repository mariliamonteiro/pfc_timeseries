import os
from flask import Flask, render_template, url_for, redirect, request
from flask_uploads import UploadSet, configure_uploads, DATA, patch_request_class
from forms import FormARIMA
from variables import *
from werkzeug.utils import secure_filename

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

    #form = FormARIMA(request.form)
    form = FormARIMA()

    if form.validate_on_submit():
        #file = request.files['dados']

        filename = secure_filename(form.dados.data.filename)
        form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        #filename = form.dados.data.filename
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #form.dados.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #filename = files.save(form.dados.data)
        file_url = files.url(form.dados.data.filename)
        return render_template('algorithms_arima_output.html', title='ARIMA', text=text, form= form, file_url=file_url)
    else:
        file_url = None

    return render_template('algorithms_arima.html', title='ARIMA', text=text, form= form, file_url=file_url)


    #
    # if (request.method == 'POST') and form.validate_on_submit():
    #     if form.data.data:
    #         result = form.data.filename
    #         return render_template('algorithms_arima_output.html', title='ARIMA', text=text, form= form, result= result)
    # else:
    #     return render_template('algorithms_arima.html', title='ARIMA', text=text, form= form)



# @app.route('/algorithms/autocorrelation')
# def algorithms_autocorrelation():
#     text = desc_list['autocorrelation']
#
#     return render_template('algorithms_arima.html', title='Autocorrelação', text=text)


# INICIAR SERVIDOR =============================================================
if __name__ == '__main__':
    app.run(debug= True)
