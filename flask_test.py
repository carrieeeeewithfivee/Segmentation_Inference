#host website on local machine, only image inference supported
import os
from flask import Flask, request, redirect, url_for,send_from_directory, render_template
from werkzeug.utils import secure_filename
import sys
from pathlib import Path
import tensorflow as tf
import shutil
import image_test
import uuid
import time

# Dataset names.
_ADE20K = 'ade20k'
_CITYSCAPES = 'cityscapes'
_MAPILLARY_VISTAS = 'mapillary_vistas'
_PASCAL = 'pascal'

#Model names
_Cityscapes_mobilenet_stride16 = 'models/mobilev2_restride16_100000.tar.gz'
_Pascal_deeplab = 'models/deeplabv3_mnv2_dm05_pascal_trainval_2018_10_01.tar.gz'
_Cityscapes_mobilenet = 'models/deeplabv3_mnv2_cityscapes_train_2018_02_05.tar.gz'
_Pascal_mobilenet = 'models/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz'

# route names
path = Path().absolute()
path = str(path).replace('\\', '/')+'/static/'
UPLOAD_FOLDER = path
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__, static_url_path = "/static", static_folder = "static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    error = None

    if request.method == 'POST':
        #choose model
        model_value = (request.form.get("selectBox"))
        print(model_value)
        # check if the post request has the file part
        if 'file' not in request.files:
            error = 'No file selected. Please try again!'
            return render_template('main.html', error = error)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            error = 'No file selected. Please try again!'
            return render_template('main.html', error = error)
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
            else:
                if model_value == "-1" : #model not selected
                    error = 'No model selected. Please try again!'
                    return render_template('main.html', error = error)
                elif (model_value == _Pascal_deeplab or model_value == _Pascal_mobilenet) : 
                    model_color = _PASCAL
                else :
                    model_color = _CITYSCAPES
                print(model_color)

                image_path = UPLOAD_FOLDER + file.filename
                output_name = str(uuid.uuid4()) + '.png'
                output_name_color = str(uuid.uuid4()) + '.png'
                duration = image_test.image_inference(model_value, image_path, model_color, output_name, output_name_color)
               
                global original_image
                original_image = file.filename

                global output_image
                output_image = output_name

                global color_image
                color_image = output_name_color

                global time_spent
                time_spent = duration
            return redirect(url_for('uploaded_file', filename=filename, color_model= model_color))
    return render_template('main.html')

@app.route('/uploads/<filename>/<color_model>')
def uploaded_file( filename, color_model):
    global original_image
    global output_image
    global color_image
    global time_spent
    return render_template("showphoto.html", original_image = original_image, bicubic_image = color_image, result_image = output_image ,time_spent=time_spent, color_model=color_model)

@app.route('/return')
def get_ses():
 	return redirect(url_for('upload_file'))

@app.route('/charts')
def get_charts():
 	return render_template("charts.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)

