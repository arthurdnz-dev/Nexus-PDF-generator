import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
from reportlab.pdfgen import canvas
from werkzeug.utils import secure_filename

app = Flask(__name__)

PDF_FOLDER = os.path.join("static", "pdfs")
os.makedirs(PDF_FOLDER, exist_ok=True)


def generate_pdf(images, output_path):
    pdf = canvas.Canvas(output_path)

    for img_file in images:
        img = Image.open(img_file)
        width, height = img.size
        pdf.setPageSize((width, height))
        pdf.drawImage(img_file, 0, 0, width, height)
        pdf.showPage()

    pdf.save()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    files = request.files.getlist("photos")

    if not files:
        return jsonify({"error": "No images received"}), 400

    temp_paths = []
    for f in files:
        filename = secure_filename(f.filename)
        temp_path = os.path.join(PDF_FOLDER, filename)
        f.save(temp_path)
        temp_paths.append(temp_path)

    output_pdf = os.path.join(PDF_FOLDER, "fotos.pdf")
    generate_pdf(temp_paths, output_pdf)

    return jsonify({
        "success": True,
        "download_url": "/download/fotos.pdf"
    })


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(PDF_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
