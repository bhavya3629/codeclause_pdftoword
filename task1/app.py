import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from pdf2docx import Converter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CONVERTED_FOLDER'] = 'static/converted'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# ...

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        output_filename = f"{filename.rsplit('.', 1)[0]}.docx"
        output_filepath = os.path.join(app.config['CONVERTED_FOLDER'], output_filename)
        convert_pdf_to_docx(filepath, output_filepath)
        return redirect(url_for('download', filename=output_filename))
    else:
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['CONVERTED_FOLDER'], filename, as_attachment=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert_pdf_to_docx(input_filepath, output_filepath):
    cv = Converter(input_filepath)
    cv.convert(output_filepath)
    cv.close()



# ...

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)
    app.run(debug=True)
