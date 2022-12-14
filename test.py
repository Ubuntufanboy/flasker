from flask import Flask, render_template, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'L'
app.config['UPLOAD_FOLDER'] = "static/files" 

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload file")

@app.route("/", methods=['GET', 'POST'])
def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        try:
            os.chdir("static/files")
        except:
            pass
        os.chdir("..")
        os.system("rm -rf files")
        os.mkdir("files")
        os.chdir("files")
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        new = file.filename.replace(".mp4", ".mp3")
        new = f"/home/apollo/projects/flasker/static/files/{new}" # hard coded for now...
        os.system(f"ffmpeg -i {file.filename} {new}")
        os.system(f"rm {file.filename}")
        return send_file(new)# Send the converted file
        os.chdir("..")
        os.chdir("..")

        return "File has been uploaded"
    return render_template("index.html", form=form)

app.run("0.0.0.0", port=5000)