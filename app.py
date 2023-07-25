from flask import Flask, render_template,redirect, url_for, request, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField
import os
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from encoder import ImageTools

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"
app.config["UPLOAD_FOLDER"] = "static/files"

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    operation = SelectField("Operation", choices=[("encode", "Encode"), ("decode", "Decode")])
    submit = SubmitField("Upload File")

@app.route("/", methods=["GET", "POST"])
def GetImage():
    form = UploadFileForm()

    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        filename = secure_filename(file.filename)
        target_folder = app.config['UPLOAD_FOLDER']
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), target_folder, filename)

        # If the file already exists, add a unique number to the filename
        counter = 1
        while os.path.exists(path):
            name, ext = os.path.splitext(filename)
            filename = f"{counter}_{name}{ext}"
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), target_folder, filename)
            counter += 1

        file.save(path)  # Then save the file

        # Get the selected operation from the form
        selected_operation = form.operation.data

        if selected_operation == "encode":
            try:
                pp = ImageTools.ImageTools().GenerateImage(path)
            except:
                return "404"
        elif selected_operation == "decode":
            try:
                pp = ImageTools.ImageTools().DecodeImage(path)
            except:
                return "404"
        else:
            return "404"

        pa = pp.split("/")[-1]
 
        return redirect(url_for("Result", image_path=pa))

    return render_template("index.html", form=form)


@app.route("/result", methods=["GET", "POST"])
def Result():
    # Get the image_path value from the query parameter
    image_path = request.args.get("image_path")
    image_name = image_path.split("/")[-1]

    # Check if the file is an image (PNG, JPEG, etc.)
    is_image = image_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))

    return render_template("output.html", image_path=image_path, is_image=is_image, image_name=image_name)

@app.route("/download/<filename>", methods=["GET"])
def DownloadFile(filename):
    file_path = os.path.join("C:/Users/PC/Desktop/ColorFile/static/output", filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)