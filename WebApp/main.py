import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)

	file = request.files['file']
	
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
		
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('home.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

#
from predictor import *
"""
model = tf.keras.models.load_model('intel_image_classifier_mobilenetv2.h5')
labels = {0: 'buildings', 1: 'forest', 2: 'glacier', 3: 'mountain', 4: 'sea', 5: 'street'}

image = trans_img('/uploads')
msg = predictor(image, labels)
"""

@app.route('/', methods=['POST'])
def submit():
	if request.method == 'POST':
		if request.form.get('Submit') == 'Submit':
			model = tf.keras.models.load_model('intel_image_classifier_mobilenetv2.h5')
			labels = {0: 'buildings', 1: 'forest', 2: 'glacier', 3: 'mountain', 4: 'sea', 5: 'street'}

			image = trans_img('static/uploads')
			msg = predictor(image, labels)
			processed_text = msg
			#return result
			return render_template('home.html', processed_text=processed_text)
	return render_template('home.html')
#

if __name__ == "__main__":
    app.run()